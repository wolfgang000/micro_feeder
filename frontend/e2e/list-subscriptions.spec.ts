import { test, expect } from "@playwright/test";
import { CreateSubscriptionPage } from "./pages-objects/create-subscription-page";
import { ListSubscriptionsPage } from "./pages-objects/list-subscriptions-page";
import { createUserAndLogin } from "./util";
import { v4 } from "uuid";

test("Show noSubscriptionsFoundMessage", async ({ page }) => {
  await createUserAndLogin(page);
  const listSubscriptionsPage = new ListSubscriptionsPage(page);
  const createSubscriptionPage = new CreateSubscriptionPage(page);
  await listSubscriptionsPage.validateCurrentUrl();

  await expect(page.locator("body")).toContainText(
    "You don't have any subscriptions yet",
  );

  await expect(listSubscriptionsPage.addSubscriptionLink).toBeVisible();
  await listSubscriptionsPage.addSubscriptionLink.click();
  createSubscriptionPage.validateCurrentUrl();

  await listSubscriptionsPage.goto();
  await expect(listSubscriptionsPage.makeSubscriptionLink).toBeVisible();
  await listSubscriptionsPage.makeSubscriptionLink.click();
  createSubscriptionPage.validateCurrentUrl();
});

test("Show user's subscriptions", async ({ page }) => {
  await createUserAndLogin(page);
  const listSubscriptionsPage = new ListSubscriptionsPage(page);
  const createSubscriptionPage = new CreateSubscriptionPage(page);
  await listSubscriptionsPage.validateCurrentUrl();
  await expect(listSubscriptionsPage.subscriptionsTable).not.toBeVisible();

  const feedUrl = `http://fake_server:9000/abcnews_usheadlines_new_items.xml`;
  const webhookUrl = `http://example-webhook.com/${v4()}`;

  await createSubscriptionPage.goto();
  await createSubscriptionPage.validateCurrentUrl();
  await createSubscriptionPage.createSubscription(feedUrl, webhookUrl);

  await listSubscriptionsPage.goto();
  await expect(listSubscriptionsPage.subscriptionsTable).toBeVisible();
  await expect(listSubscriptionsPage.subscriptionsTable).toContainText(feedUrl);
  await expect(listSubscriptionsPage.subscriptionsTable).toContainText(
    webhookUrl,
  );
});
