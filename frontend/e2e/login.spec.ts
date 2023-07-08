import { test, expect } from "@playwright/test";
import { createUserAndLogin } from "./util";

test('Click "Login With Google Button" and show google login page', async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator("#loginWithGoogleButton")).toBeVisible();
  page.locator("#loginWithGoogleButton").click();
  await page.waitForURL(/accounts.google.com/);
});

test('Already logged in redirect to subscriptions when they click the "Login With Google Button"', async ({
  page,
}) => {
  await createUserAndLogin(page);
  await page.goto("/");
  page.locator("#loginWithGoogleButton").click();
  await page.waitForURL(/subscriptions/);
});
