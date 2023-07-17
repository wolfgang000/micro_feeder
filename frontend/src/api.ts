import axios from "axios";
import env from "./env";
import { Subscription } from "./models";

const axiosInstance = axios.create({
  baseURL: env.backendUrl,
  withCredentials: true,
});

export const core = {
  createSubscription(payload: any) {
    return axiosInstance
      .post(`/web/subscriptions/`, payload)
      .then((r) => r.data as Subscription);
  },
  getSubscriptions() {
    return axiosInstance
      .get(`/web/subscriptions/`)
      .then((r) => r.data as Subscription[]);
  },
  deleteSubscription(id: number) {
    return axiosInstance.delete(`/web/subscriptions/${id}`);
  },
  logout() {
    return axiosInstance.post(`/web/auth/logout/`);
  },
};
