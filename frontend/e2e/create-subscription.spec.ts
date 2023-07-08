import { test, expect } from "@playwright/test";
import { CreateSubscriptionPage } from "./pages-objects/create-subscription-page";
import { ListSubscriptionsPage } from "./pages-objects/list-subscriptions-page";
import { createUserAndLogin } from "./util";
import { v4 } from "uuid";

test("Create subscription with valid data", async ({ page }) => {
  await createUserAndLogin(page);
  const createSubscriptionPage = new CreateSubscriptionPage(page);
  const listSubscriptionsPage = new ListSubscriptionsPage(page);
  const feedUrl = `http://example-feed.com/${v4()}`;
  const webhookUrl = `http://example-webhook.com/${v4()}`;

  await createSubscriptionPage.goto();
  await createSubscriptionPage.validateCurrentUrl();
  await createSubscriptionPage.createSubscription(feedUrl, webhookUrl);
  await listSubscriptionsPage.validateCurrentUrl();
  await expect(page.locator("body")).toContainText(feedUrl);
  await expect(page.locator("body")).toContainText(webhookUrl);
});

test("Cancel button should redirect to list subscriptions page", async ({
  page,
}) => {
  await createUserAndLogin(page);
  const createSubscriptionPage = new CreateSubscriptionPage(page);
  const listSubscriptionsPage = new ListSubscriptionsPage(page);

  await createSubscriptionPage.goto();
  await createSubscriptionPage.validateCurrentUrl();
  await createSubscriptionPage.cancelButton.click();

  await listSubscriptionsPage.validateCurrentUrl();
});
