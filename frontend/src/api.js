import { useErrorStore } from "@/stores/error.js";

// Report a failure via ErrorAlert, so that a caller can ignore it.
async function get(url) {
  let response;

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

// Return the response without reporting a failure, for a caller that renders its own errors.
function postJSON(url, body, signal) {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
}

export default { get, postJSON };
