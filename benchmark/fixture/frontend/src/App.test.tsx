import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import App from './App';

function response(page = 1) {
  return {
    ok: true,
    json: async () => ({
      items: [{
        id: `alpha-${page}`,
        title: `Incident from page ${page}`,
        status: 'open',
        severity: 'high',
        created_at: '2026-09-15T08:00:00Z',
      }],
      total: 18,
      page,
      page_size: 5,
    }),
  };
}

describe('incident list', () => {
  it('opens the URL page and sends the current workspace header', async () => {
    window.history.replaceState({}, '', '/?page=2&page_size=5');
    const fetchMock = vi.fn().mockResolvedValue(response(2));
    vi.stubGlobal('fetch', fetchMock);

    render(<App />);

    expect(await screen.findByText('Incident from page 2')).toBeTruthy();
    expect(fetchMock).toHaveBeenCalledWith('/api/incidents?page=2&page_size=5', {
      headers: { 'X-Tenant-ID': 'alpha' },
    });
    expect(screen.getByText('Page 2 of 4')).toBeTruthy();
  });

  it('navigates to the next page and preserves unrelated URL parameters', async () => {
    window.history.replaceState({}, '', '/?page=1&page_size=5&source=team');
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(response(1))
      .mockResolvedValueOnce(response(2));
    vi.stubGlobal('fetch', fetchMock);
    render(<App />);
    await screen.findByText('Incident from page 1');

    fireEvent.click(screen.getByRole('button', { name: 'Next' }));

    await waitFor(() => expect(screen.getByText('Incident from page 2')).toBeTruthy());
    const params = new URLSearchParams(window.location.search);
    expect(params.get('page')).toBe('2');
    expect(params.get('page_size')).toBe('5');
    expect(params.get('source')).toBe('team');
    expect(fetchMock).toHaveBeenLastCalledWith('/api/incidents?page=2&page_size=5', {
      headers: { 'X-Tenant-ID': 'alpha' },
    });
  });
});
