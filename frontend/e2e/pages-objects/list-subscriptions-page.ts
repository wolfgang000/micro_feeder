import { Locator, Page } from "@playwright/test";

export class ListSubscriptionsPage {
  readonly page: Page;
  readonly pagePath = "/subscriptions/";
  readonly addSubscriptionLink: Locator;
  readonly makeSubscriptionLink: Locator;
  readonly subscriptionsTable: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.addSubscriptionLink = page.getByTestId("addSubscriptionLink");
    this.makeSubscriptionLink = page.getByTestId("makeSubscriptionLink");
    this.subscriptionsTable = page.getByTestId("subscriptionsTable");
    this.logoutButton = page.getByTestId("logoutButton");
  }

  async goto() {
    await this.page.goto(this.pagePath);
  }

  async validateCurrentUrl() {
    await this.page.waitForURL(/\/subscriptions$/);
  }
}
