import { Page } from "@playwright/test";

export class ListSubscriptionsPage {
  readonly page: Page;
  readonly pagePath = "/subscriptions/";

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto(this.pagePath);
  }

  async validateCurrentUrl() {
    await this.page.waitForURL(/\/subscriptions$/);
  }
}
