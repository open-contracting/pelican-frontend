import { useErrorStore } from "@/stores/error.js";

// Requests through get() report their failure via ErrorAlert, so callers can ignore the rejection.
async function get(url) {
  let response;

  try {
    response = await fetch(url);
  } catch (error) {
    // The request never reached the server, so there is no status code.
    useErrorStore().record(0);
    throw error;
  }

  // fetch resolves whatever the status, so a failure has to be raised here.
  if (!response.ok) {
    useErrorStore().record(response.status);
    throw new Error(`${response.status} ${response.statusText}`);
  }

  return response.json();
}

// postJSON() reports nothing and returns the response, for a caller that renders its own errors.
function postJSON(url, body, signal) {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
}

export default { get, postJSON };
