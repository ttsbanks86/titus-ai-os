// BA Compass — Phase 5 Release Candidate Quality Tests

import { test, expect } from "@playwright/test";

test.describe("Release candidate quality tests", () => {
  test("landing page renders core elements", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("h1")).toBeVisible();
    await expect(page.getByRole("note", { name: "Synthetic data notice" }).first()).toBeVisible();
    await expect(page.getByText("Start 5-Minute Tour")).toBeVisible();
  });

  test("not-found page renders for unknown route", async ({ page }) => {
    await page.goto("/this-route-does-not-exist");
    // Static export returns the not-found page for unknown routes
    const body = page.locator("body");
    await expect(body).toBeVisible();
  });

  test("all primary routes respond with body", async ({ page }) => {
    const routes = ["/", "/overview", "/stakeholders", "/current-state", "/analysis", "/dashboard", "/future-state", "/requirements", "/brd", "/traceability", "/executive-summary", "/risks", "/recommendations", "/project", "/responsible-ai", "/tour"];
    for (const route of routes) {
      await page.goto(route, { waitUntil: "domcontentloaded" });
      const body = page.locator("body");
      await expect(body).toBeVisible();
    }
  });

  test("recruiter tour navigates through all steps", async ({ page }) => {
    await page.goto("/tour", { waitUntil: "domcontentloaded" });
    await expect(page.getByText("1 of 10")).toBeVisible();
    for (let i = 0; i < 9; i++) {
      await page.getByRole("button", { name: /Next/i }).click();
    }
    await expect(page.getByRole("link", { name: /Finish tour/i })).toBeVisible();
  });

  test("requirements page has edit mode button", async ({ page }) => {
    await page.goto("/requirements", { waitUntil: "domcontentloaded" });
    await expect(page.getByRole("button", { name: /Edit Demo/i }).first()).toBeVisible();
  });

  test("demo reset confirmation appears and can be cancelled", async ({ page }) => {
    await page.goto("/requirements", { waitUntil: "domcontentloaded" });
    const resetBtn = page.getByRole("button", { name: /Reset All/i });
    await expect(resetBtn).toBeVisible();
    await resetBtn.click();
    await expect(page.getByText(/reset all demo data/i)).toBeVisible();
    await page.getByRole("button", { name: /Cancel/i }).click();
  });

  test("KPI dashboard has period filter buttons", async ({ page }) => {
    await page.goto("/dashboard", { waitUntil: "domcontentloaded" });
    await expect(page.getByRole("button", { name: /Week 1/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /Week 2/i })).toBeVisible();
  });

  test("traceability page has search input", async ({ page }) => {
    await page.goto("/traceability", { waitUntil: "domcontentloaded" });
    await expect(page.locator('input[aria-label="Search traceability"]')).toBeVisible();
  });

  test("BRD page shows TOC", async ({ page }) => {
    await page.goto("/brd", { waitUntil: "domcontentloaded" });
    await expect(page.getByText("Table of Contents")).toBeVisible();
    const tocLinks = page.locator('nav[aria-label="BRD sections"] a');
    const count = await tocLinks.count();
    expect(count).toBeGreaterThanOrEqual(8);
  });

  test("risk register list is visible", async ({ page }) => {
    await page.goto("/risks", { waitUntil: "domcontentloaded" });
    await expect(page.getByText("R-001").first()).toBeVisible();
  });

  test("executive summary has key sections", async ({ page }) => {
    await page.goto("/executive-summary", { waitUntil: "domcontentloaded" });
    await expect(page.getByText("Five Strongest Findings")).toBeVisible();
    await expect(page.getByText("Priority Recommendations")).toBeVisible();
  });

  test("export buttons exist on risks page", async ({ page }) => {
    await page.goto("/risks", { waitUntil: "domcontentloaded" });
    await expect(page.getByRole("button", { name: /MD/i }).first()).toBeVisible();
  });

  test("synthetic data notice visible on key pages", async ({ page }) => {
    const routes = ["/", "/dashboard", "/brd", "/traceability", "/executive-summary", "/project", "/responsible-ai"];
    for (const route of routes) {
      await page.goto(route, { waitUntil: "domcontentloaded" });
      await expect(page.getByRole("note", { name: "Synthetic data notice" }).or(page.getByRole("note", { name: "Data notice" })).first()).toBeVisible();
    }
  });

  test("skip link is present", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator(".skip-link")).toBeVisible();
    await expect(page.locator(".skip-link")).toHaveAttribute("href", "#main-content");
  });
});
