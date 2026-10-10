const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    browserName: 'chromium',
    headless: true,
  },
  webServer: {
    command: 'python3 -m http.server 4173 --bind 127.0.0.1',
    cwd: __dirname,
    url: 'http://127.0.0.1:4173/login.html',
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});
