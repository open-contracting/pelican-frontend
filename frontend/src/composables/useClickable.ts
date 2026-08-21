import type { RouteLocationRaw } from "vue-router";
import { useRouter } from "vue-router";

export function useClickable() {
  const router = useRouter();

  /** Navigate to a route, opening a new tab if the user asked for one. Clicks on links are left to the browser. */
  function navigate(event: MouseEvent, to: RouteLocationRaw) {
    if (event.target instanceof Element && event.target.closest("a")) {
      return;
    }
    if (event.ctrlKey || event.metaKey || event.shiftKey) {
      window.open(router.resolve(to).href, "_blank");
    } else {
      router.push(to);
    }
  }

  return { navigate };
}
