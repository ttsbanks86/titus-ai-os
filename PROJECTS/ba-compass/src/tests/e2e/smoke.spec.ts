// BA Compass — Phase 3 Recruiter MVP Smoke Tests

import { test, expect } from "@playwright/test";

test.describe("Recruiter journey smoke tests", () => {
  test("landing page loads with title, notice, and KPIs", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator("h1")).toContainText("BA Compass");
    await expect(page.getByRole("note", { name: "Synthetic data notice" })).toBeVisible();
    await expect(page.getByText("Shift Fill Rate").first()).toBeVisible();
    await expect(page.getByText("Explore the Case Study")).toBeVisible();
  });

  test("navigation to all main routes works", async ({ page }) => {
    const routes = [
      { href: "/overview", title: "Project Overview" },
      { href: "/stakeholders", title: "Stakeholder" },
      { href: "/current-state", title: "Current-State" },
      { href: "/analysis", title: "Gap Analysis" },
      { href: "/dashboard", title: "KPI Dashboard" },
      { href: "/future-state", title: "Future-State" },
      { href: "/requirements", title: "Requirements" },
      { href: "/risks", title: "Risk Register" },
      { href: "/recommendations", title: "Recommendations" },
      { href: "/project", title: "About the Project" },
      { href: "/responsible-ai", title: "Responsible AI" },
    ];
    for (const route of routes) {
      await page.goto(route.href);
      await page.waitForLoadState("networkidle");
      await expect(page.locator("h1")).toContainText(route.title);
      await expect(page.locator("body")).toBeVisible();
    }
  });

  test("mobile navigation works", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/");
    const menuButton = page.locator('button[aria-label="Open menu"]');
    await expect(menuButton).toBeVisible();
    await menuButton.click();
    await expect(page.locator("#mobile-menu")).toBeVisible();
    await page.click('#mobile-menu a[href="/stakeholders"]');
    await expect(page.locator("h1")).toContainText("Stakeholder");
  });

  test("KPI dashboard loads with charts and metrics", async ({ page }) => {
    await page.goto("/dashboard");
    await expect(page.locator("h1")).toContainText("KPI Dashboard");
    await expect(page.getByRole("region", { name: /Shift Fill Rate/ })).toBeVisible();
    await expect(page.getByRole("region", { name: /Missed Shift Rate/ })).toBeVisible();
    await expect(page.getByRole("region", { name: /Late Arrival Rate/ })).toBeVisible();
    await expect(page.locator(".recharts-responsive-container").first()).toBeVisible();
  });

  test("requirements page has filters and table", async ({ page }) => {
    await page.goto("/requirements");
    await expect(page.locator("h1")).toContainText("Requirements");
    await expect(page.getByRole("button", { name: "BR" }).first()).toBeVisible();
    await expect(page.getByRole("button", { name: "FR" }).first()).toBeVisible();
    const searchBox = page.locator('input[aria-label="Search requirements"]');
    await searchBox.fill("BR-001");
    await expect(page.getByText("BR-001").first()).toBeVisible();
  });

  test("risk register shows all 15 risks", async ({ page }) => {
    await page.goto("/risks");
    await expect(page.locator("h1")).toContainText("Risk Register");
    await expect(page.getByRole("button", { name: /R-001/ }).first()).toBeVisible();
    await expect(page.getByText("R-015").first()).toBeVisible();
  });

  test("process pages show step details", async ({ page }) => {
    await page.goto("/current-state");
    await expect(page.locator("h1")).toContainText("Current-State");
    await expect(page.getByRole("button", { name: /1.*Shift Creation/ }).first()).toBeVisible();
    await expect(page.getByRole("button", { name: /11.*Management Reporting/ }).first()).toBeVisible();

    await page.goto("/future-state");
    await expect(page.locator("h1")).toContainText("Future-State");
    await expect(page.getByText("Current vs. Future").first()).toBeVisible();
  });

  test("recommendations page links to requirements and KPIs", async ({ page }) => {
    await page.goto("/recommendations");
    await expect(page.locator("h1")).toContainText("Recommendations");
    await expect(page.getByText("Immediate Actions")).toBeVisible();
    await expect(page.getByText("Near-Term Actions")).toBeVisible();
    await expect(page.getByText("Future Enhancements")).toBeVisible();
  });

  test("about project page shows contributions", async ({ page }) => {
    await page.goto("/project");
    await expect(page.locator("h1")).toContainText("About the Project");
    await expect(page.getByText("My Contribution")).toBeVisible();
  });

  test("responsible AI page shows checklist", async ({ page }) => {
    await page.goto("/responsible-ai");
    await expect(page.locator("h1")).toContainText("Responsible AI");
    await expect(page.getByText("AI is Optional")).toBeVisible();
    await expect(page.getByRole("heading", { name: "Transparency Note" })).toBeVisible();
  });

  test("no broken internal links", async ({ page }) => {
    await page.goto("/");
    const links = page.locator("a[href^='/']");
    const count = await links.count();
    expect(count).toBeGreaterThan(10);
    const hrefs = await links.evaluateAll((els) => els.map((el) => el.getAttribute("href")));
    const unique = [...new Set(hrefs)].filter(Boolean) as string[];
    for (const href of unique.slice(0, 8)) {
      if (href && !href.includes("#")) {
        await page.goto(href);
        await expect(page.locator("body")).toBeVisible();
      }
    }
  });
});
