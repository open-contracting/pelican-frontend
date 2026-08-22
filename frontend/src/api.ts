import { useErrorStore } from "@/stores/error.js";

/** The response body, if the request succeeded, or the status that explains why it didn't. */
type PostResult<T> = { ok: true; data: T } | { ok: false; status: number; statusText: string };

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

// Callers need to handle errors. Use this for an endpoint that returns no body to parse.
function post(url: string, body: unknown, signal?: AbortSignal) {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
}

// Callers need to handle errors.
async function postJSON<T>(url: string, body: unknown, signal?: AbortSignal): Promise<PostResult<T>> {
  const response = await post(url, body, signal);

  if (!response.ok) {
    return { ok: false, status: response.status, statusText: response.statusText };
  }

  return { ok: true, data: await response.json() };
}

export default { get, post, postJSON };
