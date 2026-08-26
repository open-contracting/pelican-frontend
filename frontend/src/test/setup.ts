// Node defines a localStorage global that is unavailable without --localstorage-file, and it shadows
// the one happy-dom would provide. Install a working implementation, so tests behave like a browser.
class MemoryStorage implements Storage {
  #items = new Map<string, string>();

  get length() {
    return this.#items.size;
  }

  key(index: number) {
    return [...this.#items.keys()][index] ?? null;
  }

  getItem(key: string) {
    return this.#items.get(key) ?? null;
  }

  setItem(key: string, value: string) {
    this.#items.set(key, String(value));
  }

  removeItem(key: string) {
    this.#items.delete(key);
  }

  clear() {
    this.#items.clear();
  }
}

for (const target of [globalThis, window]) {
  Object.defineProperty(target, "localStorage", { value: new MemoryStorage(), configurable: true, writable: true });
}
