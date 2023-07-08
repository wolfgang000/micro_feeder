import axios from "axios";
import env from "./env";

const axiosInstance = axios.create({
  baseURL: env.backendUrl,
  withCredentials: true,
});

export const core = {
  createSubscription(payload: any) {
    return axiosInstance
      .post(`/web/subscriptions/`, payload)
      .then((r) => r.data);
  },
  getSubscriptionas() {
    return axiosInstance.get(`/web/subscriptions/`).then((r) => r.data);
  },
};
