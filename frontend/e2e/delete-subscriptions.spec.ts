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

  const feedUrl1 = `http://fake_server:9000/abcnews_usheadlines.xml`;
  const feedUrl2 = `http://fake_server:9000/abcnews_usheadlines_new_items.xml`;

  await createSubscriptionPage.goto();
  await createSubscriptionPage.createSubscription(
    feedUrl1,
    `http://example-webhook.com/${v4()}`
  );
  await listSubscriptionsPage.validateCurrentUrl();

  await createSubscriptionPage.goto();
  await createSubscriptionPage.createSubscription(
    feedUrl2,
    `http://example-webhook.com/${v4()}`
  );
  await listSubscriptionsPage.validateCurrentUrl();

  await listSubscriptionsPage.goto();
  await expect(listSubscriptionsPage.subscriptionsTable).toBeVisible();
  await expect(listSubscriptionsPage.subscriptionsTable).toContainText(
    feedUrl1
  );
  await expect(listSubscriptionsPage.subscriptionsTable).toContainText(
    feedUrl2
  );
  //-----------------------------------
  // Select and delete feedUrl1
  const selectedRow = listSubscriptionsPage.subscriptionsTable.locator(
    `//td[contains(text(), "${feedUrl1}")]/..`
  );

  const selectedRowDeleteButton = selectedRow.locator(
    `//button[contains(text(), "Delete")]`
  );
  await expect(selectedRowDeleteButton).toBeVisible();
  await selectedRowDeleteButton.click();

  await expect(listSubscriptionsPage.confirmDeleteModal).toBeVisible();
  await expect(
    listSubscriptionsPage.deleteSubscriptionButtonModal
  ).toBeVisible();
  await listSubscriptionsPage.deleteSubscriptionButtonModal.click();

  //--------
  // Show feedUrl2 but not feedUrl1
  await expect(listSubscriptionsPage.subscriptionsTable).not.toContainText(
    feedUrl1
  );
  await expect(listSubscriptionsPage.subscriptionsTable).toContainText(
    feedUrl2
  );
});
