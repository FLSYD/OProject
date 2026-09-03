const { defineConfig } = require('@playwright/test')

const python = process.env.E2E_PYTHON || 'python'

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  workers: 1,
  use: { baseURL: 'http://127.0.0.1:18080', trace: 'retain-on-failure' },
  webServer: [
    { command: `${python} manage.py run_e2e`, cwd: '../backend', url: 'http://127.0.0.1:18000/api/health/', reuseExistingServer: false, timeout: 120000 },
    { command: 'npm run serve -- --host 127.0.0.1 --port 18080 --mode e2e', cwd: '.', url: 'http://127.0.0.1:18080', reuseExistingServer: false, timeout: 120000 }
  ],
  projects: [{ name: 'chromium', use: { browserName: 'chromium' } }]
})
