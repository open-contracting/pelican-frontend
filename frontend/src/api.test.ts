import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";
import api from "@/api.js";
import { useErrorStore } from "@/stores/error.js";

const fetchMock = vi.fn();

function respondWith(body: unknown, init: { ok?: boolean; status?: number; statusText?: string } = {}) {
  const { ok = true, status = 200, statusText = "OK" } = init;
  fetchMock.mockResolvedValueOnce({ ok, status, statusText, json: async () => body } as Response);
}

beforeEach(() => {
  setActivePinia(createPinia());
  fetchMock.mockReset();
  vi.stubGlobal("fetch", fetchMock);
});

describe("get", () => {
  it("returns the parsed body, recording no error", async () => {
    respondWith({ id: 1 });

    expect(await api.get("/api/datasets/1")).toEqual({ id: 1 });
    expect(useErrorStore().status).toBeNull();
  });

  it("records the status of a rejected request, and throws", async () => {
    respondWith(null, { ok: false, status: 403, statusText: "Forbidden" });

    await expect(api.get("/api/datasets/1")).rejects.toThrow("403 Forbidden");
    expect(useErrorStore().status).toBe(403);
  });

  it("records 0 when the request never reached the server, and throws", async () => {
    fetchMock.mockRejectedValueOnce(new TypeError("Failed to fetch"));

    await expect(api.get("/api/datasets/1")).rejects.toThrow("Failed to fetch");
    expect(useErrorStore().status).toBe(0);
  });
});

describe("patch", () => {
  it("sends the body as JSON", async () => {
    respondWith(null);

    await api.patch("/api/settings/", { language: "es" });

    expect(fetchMock).toHaveBeenCalledWith("/api/settings/", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: '{"language":"es"}',
    });
  });

  it("records the status of a rejected request", async () => {
    respondWith(null, { ok: false, status: 500, statusText: "Server Error" });

    await expect(api.patch("/api/settings/", {})).rejects.toThrow("500 Server Error");
    expect(useErrorStore().status).toBe(500);
  });
});

describe("postJSON", () => {
  it("returns the parsed body of a successful response", async () => {
    respondWith({ items: 3 });

    expect(await api.postJSON("/api/dataset-filter-items/", { dataset_id_original: 7 })).toEqual({
      ok: true,
      data: { items: 3 },
    });
  });

  it("returns the status of a failed response, for the caller to report", async () => {
    respondWith(null, { ok: false, status: 400, statusText: "Bad Request" });

    expect(await api.postJSON("/api/generate-report", {})).toEqual({
      ok: false,
      status: 400,
      statusText: "Bad Request",
    });
    // The caller reports this failure itself, so the shared alert stays quiet.
    expect(useErrorStore().status).toBeNull();
  });

  it("passes an abort signal through", async () => {
    respondWith({ items: 0 });
    const controller = new AbortController();

    await api.postJSON("/api/dataset-filter-items/", {}, controller.signal);

    expect(fetchMock.mock.calls[0][1]).toMatchObject({ method: "POST", signal: controller.signal });
  });
});

describe("the error store", () => {
  it("keeps the most recent failure until it is dismissed", async () => {
    const store = useErrorStore();
    respondWith(null, { ok: false, status: 404, statusText: "Not Found" });
    respondWith(null, { ok: false, status: 500, statusText: "Server Error" });

    await expect(api.get("/a")).rejects.toThrow();
    await expect(api.get("/b")).rejects.toThrow();
    expect(store.status).toBe(500);

    store.clear();
    expect(store.status).toBeNull();
  });
});
