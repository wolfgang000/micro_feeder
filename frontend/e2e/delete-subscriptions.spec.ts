import { test, expect } from "@playwright/test";
import { CreateSubscriptionPage } from "./pages-objects/create-subscription-page";
import { ListSubscriptionsPage } from "./pages-objects/list-subscriptions-page";
import { createUserAndLogin } from "./util";
import { v4 } from "uuid";

test("delete subscription", async ({ page }) => {
  await createUserAndLogin(page);
  const listSubscriptionsPage = new ListSubscriptionsPage(page);
  const createSubscriptionPage = new CreateSubscriptionPage(page);
  await listSubscriptionsPage.validateCurrentUrl();
  await expect(listSubscriptionsPage.subscriptionsTable).not.toBeVisible();

  const feedUrl1 = `http://example-feed.com/${v4()}`;
  const feedUrl2 = `http://example-feed.com/${v4()}`;

  await createSubscriptionPage.goto();
  await createSubscriptionPage.createSubscription(
    feedUrl1,
    `http://example-webhook.com/${v4()}`
  );
  await createSubscriptionPage.goto();
  await createSubscriptionPage.createSubscription(
    feedUrl2,
    `http://example-webhook.com/${v4()}`
  );

  await listSubscriptionsPage.goto();
  await expect(listSubscriptionsPage.subscriptionsTable).toBeVisible();
  await expect(listSubscriptionsPage.subscriptionsTable).toContainText(
    feedUrl1
  );
  await expect(listSubscriptionsPage.subscriptionsTable).toContainText(
    feedUrl2
  );
});
