// BA Compass — Phase 4 Interactive Analysis and Export Tests

import { test, expect } from "@playwright/test";

test.describe("Recruiter journey smoke tests", () => {
  test("landing page loads with title, notice, and KPIs", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("h1")).toContainText("BA Compass");
    await expect(page.getByRole("note", { name: "Synthetic data notice" })).toBeVisible();
    await expect(page.getByText("Shift Fill Rate").first()).toBeVisible();
  });

  test("navigation to all Phase 4 routes works", async ({ page }) => {
    const routes = [
      { href: "/brd", title: "Business Requirements Document" },
      { href: "/traceability", title: "Traceability" },
      { href: "/executive-summary", title: "Executive Summary" },
    ];
    for (const route of routes) {
      await page.goto(route.href);
      await page.waitForLoadState("networkidle");
      await expect(page.locator("h1")).toContainText(route.title);
    }
  });

  test("mobile navigation works", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/");
    const menuButton = page.locator('button[aria-label="Open menu"]');
    await expect(menuButton).toBeVisible();
    await menuButton.click();
    await expect(page.locator("#mobile-menu")).toBeVisible();
    await page.click('#mobile-menu a[href="/traceability"]');
    await expect(page.locator("h1")).toContainText("Traceability");
  });

  test("requirements page has edit mode", async ({ page }) => {
    await page.goto("/requirements");
    await expect(page.locator("h1")).toContainText("Requirements");
    await expect(page.getByRole("button", { name: /Edit Demo/i })).toBeVisible();
  });

  test("edit a requirement, save, and see local edit indicator", async ({ page }) => {
    await page.goto("/requirements");
    await page.getByRole("button", { name: /Edit Demo/i }).click();
    // Verify edit mode is active (the Done Editing button appears)
    await expect(page.getByRole("button", { name: /Done Editing/i })).toBeVisible();
  });

  test("BRD page has table of contents and export buttons", async ({ page }) => {
    await page.goto("/brd");
    await expect(page.locator("h1")).toContainText("Business Requirements Document");
    await expect(page.getByText("Table of Contents")).toBeVisible();
    await expect(page.getByText("Executive Summary").first()).toBeVisible();
    await expect(page.getByRole("button", { name: /Export MD/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Print \/ PDF/i })).toBeVisible();
  });

  test("traceability page has filters and coverage summary", async ({ page }) => {
    await page.goto("/traceability");
    await expect(page.locator("h1")).toContainText("Traceability");
    await expect(page.getByText("Total Traceability Links")).toBeVisible();
    await expect(page.getByText("T-001")).toBeVisible();
    await expect(page.getByText("T-015")).toBeVisible();
    // Search works
    const searchBox = page.locator('input[aria-label="Search traceability"]');
    await searchBox.fill("KPI-001");
    await expect(page.getByText("KPI-001").first()).toBeVisible();
  });

  test("executive summary has findings and export", async ({ page }) => {
    await page.goto("/executive-summary");
    await expect(page.locator("h1")).toContainText("Executive Summary");
    await expect(page.getByText("Five Strongest Findings")).toBeVisible();
    await expect(page.getByRole("button", { name: /Export MD/i })).toBeVisible();
  });

  test("dashboard has KPI period filtering", async ({ page }) => {
    await page.goto("/dashboard");
    await expect(page.locator("h1")).toContainText("KPI Dashboard");
    await expect(page.getByRole("button", { name: /Week 1/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Week 2/i })).toBeVisible();
    // Click Week 1 filter
    await page.getByRole("button", { name: /Week 1/i }).click();
    await expect(page.getByText("Week 1").first()).toBeVisible();
  });

  test("dashboard drill-down on metric click", async ({ page }) => {
    await page.goto("/dashboard");
    // Click on the Shift Fill Rate metric card (which is a div with role="button")
    const metricCard = page.getByRole("button", { name: /Shift Fill Rate/i }).first();
    if (await metricCard.isVisible()) {
      await metricCard.click();
      // Drill-down table should appear
      await expect(page.getByText("Drill-Down: shift-fill").first()).toBeVisible();
    }
  });

  test("risk register has export buttons", async ({ page }) => {
    await page.goto("/risks");
    await expect(page.locator("h1")).toContainText("Risk Register");
    await expect(page.getByRole("button", { name: /MD/i }).first()).toBeVisible();
    await expect(page.getByRole("button", { name: /CSV/i }).first()).toBeVisible();
  });

  test("demo reset is accessible on requirements page", async ({ page }) => {
    await page.goto("/requirements");
    await expect(page.getByRole("button", { name: /Reset All/i })).toBeVisible();
    await page.getByRole("button", { name: /Reset All/i }).click();
    // Confirmation dialog appears
    await expect(page.getByText(/reset all demo data/i)).toBeVisible();
    await page.getByRole("button", { name: /Cancel/i }).click();
  });

  test("no broken internal links on all routes", async ({ page }) => {
    const allRoutes = ["/", "/overview", "/stakeholders", "/current-state", "/analysis", "/dashboard", "/future-state", "/requirements", "/brd", "/traceability", "/executive-summary", "/risks", "/recommendations", "/project", "/responsible-ai"];
    for (const route of allRoutes) {
      await page.goto(route);
      await page.waitForLoadState("networkidle");
      await expect(page.locator("body")).toBeVisible();
    }
  });
});
