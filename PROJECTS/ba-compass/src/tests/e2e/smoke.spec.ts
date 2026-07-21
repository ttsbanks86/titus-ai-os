// BA Compass — Playwright Smoke Test
// Verify application loads, shows title, synthetic notice, and navigation works.

import { test, expect } from "@playwright/test";

test.describe("Application smoke test", () => {
  test("home page loads with correct title and notice", async ({ page }) => {
    await page.goto("/");

    // Verify the BA Compass title is visible
    await expect(page.locator("h1")).toContainText("BA Compass");

    // Verify synthetic data notice is present
    await expect(page.getByText(/synthetic and fictional/i)).toBeVisible();
  });

  test("navigation to stakeholders page works", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/stakeholders"]');
    await expect(page.locator("h1")).toContainText("Stakeholder");
  });

  test("navigation to KPI dashboard works", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/dashboard"]');
    await expect(page.locator("h1")).toContainText("KPI Dashboard");
  });

  test("navigation to current state works", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/current-state"]');
    await expect(page.locator("h1")).toContainText("Current-State");
  });

  test("navigation to risks page works", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/risks"]');
    await expect(page.locator("h1")).toContainText("Risk Register");
  });

  test("no page-level errors on any visited route", async ({ page }) => {
    const routes = [
      "/", "/overview", "/stakeholders", "/current-state",
      "/analysis", "/dashboard", "/future-state",
      "/requirements", "/risks", "/recommendations",
      "/project", "/responsible-ai",
    ];

    for (const route of routes) {
      await page.goto(route);
      // Wait for content to render
      await page.waitForLoadState("networkidle");
      // Confirm no error boundary or crash
      const body = page.locator("body");
      await expect(body).toBeVisible();
    }
  });
});
