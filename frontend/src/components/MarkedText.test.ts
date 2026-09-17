import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";
import MarkedText from "@/components/MarkedText.vue";

describe("MarkedText", () => {
  it("renders the segments seamlessly, marking the matched ones", () => {
    const wrapper = mount(MarkedText, {
      props: {
        segments: [
          { text: "tender", matched: true },
          { text: ".items.", matched: false },
          { text: "tender", matched: true },
          { text: "s", matched: false },
        ],
      },
    });

    // The joined text must not gain whitespace between segments.
    expect(wrapper.text()).toBe("tender.items.tenders");
    expect(wrapper.html()).toContain("<mark>tender</mark>");
  });

  it("renders an unmatched path without any mark", () => {
    const wrapper = mount(MarkedText, { props: { segments: [{ text: "tender.items", matched: false }] } });

    expect(wrapper.text()).toBe("tender.items");
    expect(wrapper.html()).not.toContain("<mark>");
  });
});
