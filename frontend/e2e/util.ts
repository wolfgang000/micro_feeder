import { Page } from "@playwright/test";
import env from "../src/env";
import { v4 } from "uuid";

export const createUserAndLogin = async (page: Page) => {
  const userEmail = `${v4()}@example.com`;
  await page.goto(
    `${
      env.backendUrl || "http://localhost:8001"
    }/testing/create_user_and_login/?user_email=${userEmail}`
  );
  await page.waitForURL(/dashboard/);
};
