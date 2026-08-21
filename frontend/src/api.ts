import { useErrorStore } from "@/stores/error.js";

// This reports an error via ErrorAlert. Callers don't need to handle errors.
async function get<T>(url: string): Promise<T> {
  let response: Response;

  try {
    response = await fetch(url);
  } catch (error) {
    // The request never reached the server, so there is no status code.
    useErrorStore().record(0);
    throw error;
  }

  if (!response.ok) {
    useErrorStore().record(response.status);
    throw new Error(`${response.status} ${response.statusText}`);
  }

  return response.json();
}

// Callers need to handle errors.
function postJSON(url: string, body: unknown, signal?: AbortSignal) {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
}

export default { get, postJSON };
