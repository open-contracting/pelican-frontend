import { defineStore } from "pinia";
import { ref } from "vue";

export const useErrorStore = defineStore("error", () => {
  // The most recent failed request: its status code, or 0 if it never reached the server. null if there is none.
  const status = ref<number | null>(null);

  function record(statusCode: number) {
    status.value = statusCode;
  }

  function clear() {
    status.value = null;
  }

  return { status, record, clear };
});
