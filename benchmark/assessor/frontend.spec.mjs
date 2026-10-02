// Independent, frozen behavioral checks. Never copy this directory into A/B.
import { test, expect } from '@playwright/test';

const idsByStatus = {
  open: [16, 13, 10, 7, 4, 1],
  in_progress: [17, 14, 11, 8, 5, 2],
  closed: [18, 15, 12, 9, 6, 3],
};
const incidentId = (id, tenant = 'alpha') => `${tenant}-${String(id).padStart(3, '0')}`;
const statusControl = (page) => page.getByRole('combobox', { name: 'Status', exact: true });
const requestStatus = (request) => new URL(request.url()).searchParams.get('status');
const payload = (status) => ({
  items: idsByStatus[status].slice(0, 5).map((id) => ({
    id: incidentId(id),
    title: `Assessor incident ${String(id).padStart(3, '0')}`, status, severity: 'medium', created_at: '2026-01-01T12:00:00Z',
  })),
  total: 6, page: 1, page_size: 5,
});

async function visibleIncidents(page, expected, absent = []) {
  for (const id of expected) await expect(page.getByText(incidentId(id), { exact: true })).toBeVisible();
  for (const id of absent) await expect(page.getByText(incidentId(id), { exact: true })).toHaveCount(0);
}

async function hasQuery(page, name, expected) {
  await expect.poll(() => new URL(page.url()).searchParams.get(name)).toBe(expected);
}

test('URL status and page restore the control and matching server results on reload', async ({ page }) => {
  await page.goto('/?status=closed&page=2&page_size=2');
  await expect(statusControl(page)).toHaveValue('closed');
  await visibleIncidents(page, [12, 9], [16, 15]);
  await page.reload();
  await expect(statusControl(page)).toHaveValue('closed');
  await visibleIncidents(page, [12, 9], [16, 15]);
});

test('changing status resets page, keeps page size, and Next preserves the filter', async ({ page }) => {
  await page.goto('/?page=3&page_size=2');
  await visibleIncidents(page, [14, 13]);
  await statusControl(page).selectOption('open');
  await hasQuery(page, 'page', '1');
  await hasQuery(page, 'page_size', '2');
  await hasQuery(page, 'status', 'open');
  await visibleIncidents(page, [16, 13], [18, 17]);
  await page.getByRole('button', { name: 'Next', exact: true }).click();
  await hasQuery(page, 'page', '2');
  await hasQuery(page, 'status', 'open');
  await expect(statusControl(page)).toHaveValue('open');
  await visibleIncidents(page, [10, 7], [16, 13]);
  await page.getByRole('button', { name: 'Previous', exact: true }).click();
  await hasQuery(page, 'page', '1');
  await hasQuery(page, 'status', 'open');
  await hasQuery(page, 'page_size', '2');
  await visibleIncidents(page, [16, 13], [10, 7]);
});

test('All clears status and resets pagination', async ({ page }) => {
  await page.goto('/?status=closed&page=2&page_size=2');
  await expect(statusControl(page)).toHaveValue('closed');
  await statusControl(page).selectOption({ label: 'All' });
  await hasQuery(page, 'status', null);
  await hasQuery(page, 'page', '1');
  await visibleIncidents(page, [18, 17], [12, 9]);
});

test('In progress is an available status with matching results', async ({ page }) => {
  await page.goto('/');
  await statusControl(page).selectOption('in_progress');
  await hasQuery(page, 'status', 'in_progress');
  await visibleIncidents(page, [17, 14, 11, 8, 5], [18, 16]);
});

test('the labeled native select has all options and is reachable with Tab', async ({ page }) => {
  await page.goto('/');
  const control = statusControl(page);
  await expect(control).toHaveJSProperty('tagName', 'SELECT');
  await expect(control.locator('option')).toHaveText(['All', 'Open', 'In progress', 'Closed']);
  let reached = false;
  for (let index = 0; index < 15; index += 1) {
    await page.keyboard.press('Tab');
    if (await control.evaluate((element) => document.activeElement === element)) {
      reached = true;
      break;
    }
  }
  expect(reached).toBe(true);
});

test('switching tenant keeps the active filter and does not render alpha results', async ({ page }) => {
  await page.goto('/?status=open&page=1');
  await visibleIncidents(page, [16, 13, 10, 7, 4]);
  await page.getByRole('combobox', { name: 'Workspace', exact: true }).selectOption('beta');
  await expect(statusControl(page)).toHaveValue('open');
  for (const id of [7, 4, 1]) {
    await expect(page.getByText(incidentId(id, 'beta'), { exact: true })).toBeVisible();
  }
  await visibleIncidents(page, [], [16, 13, 10, 7, 4]);
});

test('loading and empty states remain visible for filtered requests', async ({ page }) => {
  let release;
  const gate = new Promise((resolve) => { release = resolve; });
  await page.route('**/api/incidents**', async (route) => {
    await gate;
    await route.fulfill({ status: 200, json: payload('open') });
  });
  await page.goto('/?status=open');
  await expect(page.getByText('Loading incidents…', { exact: true })).toBeVisible();
  await expect(statusControl(page)).toBeEnabled();
  release();
  await visibleIncidents(page, [16]);
  await page.unroute('**/api/incidents**');
  await page.goto('/?status=open&page=99');
  await expect(page.getByText('No incidents found.', { exact: true })).toBeVisible();
  await expect(page.getByRole('alert')).toHaveCount(0);
});

test('a filtered request error stays an error and Retry recovers the same filter', async ({ page }) => {
  await page.route('**/api/incidents**', (route) => route.fulfill({ status: 503, json: { detail: 'Unavailable' } }));
  await page.goto('/?status=closed');
  await expect(page.getByRole('alert')).toContainText('Unable to load incidents. Please try again.');
  await expect(page.getByText('No incidents found.', { exact: true })).toHaveCount(0);
  await page.unroute('**/api/incidents**');
  await page.getByRole('button', { name: 'Retry', exact: true }).click();
  await visibleIncidents(page, [18, 15, 12, 9, 6], [17, 16]);
  await expect(statusControl(page)).toHaveValue('closed');
  await expect(page.getByRole('alert')).toHaveCount(0);
});

for (const staleError of [false, true]) {
  test(`latest filter wins over a late ${staleError ? 'error' : 'successful response'}`, async ({ page }) => {
    await page.goto('/');
    await visibleIncidents(page, [18]);
    let started;
    let finished;
    const firstStarted = new Promise((resolve) => { started = resolve; });
    const firstFinished = new Promise((resolve) => { finished = resolve; });
    const oldRequestSettled = new Promise((resolve) => {
      const settle = (request) => {
        if (request.url().includes('/api/incidents') && requestStatus(request) === 'open') resolve();
      };
      page.on('requestfinished', settle);
      page.on('requestfailed', settle);
    });
    await page.route('**/api/incidents**', async (route) => {
      const status = requestStatus(route.request());
      if (status === 'open') {
        started();
        await new Promise((resolve) => setTimeout(resolve, 600));
        try {
          await route.fulfill(staleError
            ? { status: 503, json: { detail: 'Old request failed' } }
            : { status: 200, json: payload('open') });
        } catch (error) {
          // Aborting the superseded request is a valid latest-response strategy.
          if (!/closed|cancel|abort|disposed|invalid interception/i.test(String(error))) throw error;
        } finally {
          finished();
        }
      } else if (status === 'closed') {
        await route.fulfill({ status: 200, json: payload('closed') });
      } else {
        await route.continue();
      }
    });
    await statusControl(page).selectOption('open');
    await firstStarted;
    await statusControl(page).selectOption('closed');
    await visibleIncidents(page, [18, 15, 12, 9, 6], [16, 13]);
    await firstFinished;
    await oldRequestSettled;
    // Network completion alone can precede the JSON handler and React render.
    await page.evaluate(() => new Promise((resolve) => {
      requestAnimationFrame(() => requestAnimationFrame(resolve));
    }));
    await expect(statusControl(page)).toHaveValue('closed');
    await visibleIncidents(page, [18, 15, 12, 9, 6], [16, 13]);
    await expect(page.getByRole('alert')).toHaveCount(0);
  });
}
