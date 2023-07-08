import { test, expect } from "@playwright/test";
import { CreateSubscriptionPage } from "./pages-objects/create-subscription-page";
import { ListSubscriptionsPage } from "./pages-objects/list-subscriptions-page";
import { createUserAndLogin } from "./util";

test("Create subscription with valid data", async ({ page }) => {
  await createUserAndLogin(page);
  const createSubscriptionPage = new CreateSubscriptionPage(page);
  const listSubscriptionsPage = new ListSubscriptionsPage(page);

  await createSubscriptionPage.goto();
  await createSubscriptionPage.validateCurrentUrl();
  await createSubscriptionPage.createSubscription(
    "http://example.com/",
    "http://example.com/"
  );
  await listSubscriptionsPage.validateCurrentUrl();
});
