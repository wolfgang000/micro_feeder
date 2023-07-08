import { expect, Locator, Page } from "@playwright/test";

export class CreateSubscriptionPage {
  readonly page: Page;
  readonly pagePath = "/subscriptions/add";
  readonly feedUrlField: Locator;
  readonly webhookUrlField: Locator;
  readonly cancelButton: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.feedUrlField = page.locator("#createSubscriptionFeedUrlField");
    this.webhookUrlField = page.locator("#createSubscriptionWebhookUrlField");
    this.cancelButton = page.locator("#createSubscriptionCancelButton");
    this.submitButton = page.locator("#createSubscriptionSubmitButton");
  }

  async goto() {
    await this.page.goto(this.pagePath);
  }

  async validateCurrentUrl() {
    await this.page.waitForURL(/\/subscriptions\/add/);
  }

  async createSubscription(feedUrl: string, webhookUrl: string) {
    await expect(this.feedUrlField).toBeVisible();
    await expect(this.webhookUrlField).toBeVisible();
    await this.feedUrlField.fill(feedUrl);
    await this.webhookUrlField.fill(webhookUrl);
    await this.submitButton.click();
  }
}
