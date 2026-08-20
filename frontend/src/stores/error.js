import { defineStore } from "pinia";
import { ref } from "vue";

export const useErrorStore = defineStore("error", () => {
  // The most recent failed request: its status code, or 0 if it never reached the server. null if there is none.
  const status = ref(null);

  function record(error) {
    status.value = error.response?.status ?? 0;
  }

  function clear() {
    status.value = null;
  }

  return { status, record, clear };
});
