import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./src/tests/e2e",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:4173",
    trace: "on-first-retry",
    actionTimeout: 10000,
  },
  webServer: [
    {
      command: "npx serve@latest out -l 4173 --no-clipboard",
      url: "http://localhost:4173",
      reuseExistingServer: !process.env.CI,
      timeout: 30000,
    },
  ],
  timeout: 60000,
});
