import { test, expect } from "@playwright/test";
import { ListSubscriptionsPage } from "./pages-objects/list-subscriptions-page";
import { createUserAndLogin } from "./util";

test("Click Logout Button and redirect to landing page", async ({ page }) => {
  await createUserAndLogin(page);
  const listSubscriptionsPage = new ListSubscriptionsPage(page);
  await listSubscriptionsPage.validateCurrentUrl();
  await expect(listSubscriptionsPage.logoutButton).toBeVisible();
  await listSubscriptionsPage.logoutButton.click();

  page.waitForURL(/\/$/);
  await expect(page.locator("#loginWithGoogleButton")).toBeVisible();
  page.locator("#loginWithGoogleButton").click();
  await page.waitForURL(/accounts.google.com/);
});
