import axios from "axios";
import { useErrorStore } from "@/stores/error.js";

// Requests through this instance report their failure via ErrorAlert, so callers can ignore the rejection.
// Use axios directly where the caller renders its own error.
const api = axios.create();

api.interceptors.response.use(null, (error) => {
  useErrorStore().record(error);
  return Promise.reject(error);
});

export default api;
