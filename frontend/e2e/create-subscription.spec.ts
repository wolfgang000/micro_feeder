import { test, expect } from "@playwright/test";
import { CreateSubscriptionPage } from "./pages-objects/create-subscription-page";
import { createUserAndLogin } from "./util";

test("Create subscription with valid data", async ({ page }) => {
  await createUserAndLogin(page);
  const createSubscriptionPage = new CreateSubscriptionPage(page);
  await createSubscriptionPage.goto();
  await createSubscriptionPage.validateCurrentUrl();
  await createSubscriptionPage.createSubscription(
    "http://example.com/",
    "http://example.com/"
  );
});
