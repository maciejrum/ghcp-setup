import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'frontend.spec.mjs',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 15_000,
  reporter: [['list'], ['json', { outputFile: process.env.ASSESSOR_REPORT || 'test-results/frontend.json' }]],
  use: {
    baseURL: process.env.FRONTEND_URL || 'http://127.0.0.1:5173',
    browserName: 'chromium',
    ...(process.env.ASSESSOR_BROWSER_CHANNEL ? { channel: process.env.ASSESSOR_BROWSER_CHANNEL } : {}),
    trace: 'retain-on-failure',
  },
});
