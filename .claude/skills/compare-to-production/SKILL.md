---
name: compare-to-production
description: Find visual and behavioural differences between a local pelican-frontend branch and pelican.open-contracting.org, which runs main. Use when asked to test, QA, or regression-check the frontend, to compare dev to production, or to investigate a layout, styling, or render difference between the two.
---

# Comparing dev to production

Both sides read the same database, so dataset IDs match and pages are directly comparable.

`docs/contributing/compare-to-production.rst` carries what a human also needs: the endpoints that
must never be triggered, how to configure `.env`, how to choose datasets, and the route checklist.
**Read it first** — the safety section is not optional, and the browsing you do here reaches a
production database. This file is the technique for driving the comparison from a terminal.

Written during the Vue 2 → 3 migration. The techniques generalise; the specifics (ports, class
names, which datasets have which checks) may not.

## Setup

Backend on :8000, frontend on :8080:

```bash
nohup uv run --env-file .env manage.py runserver > /tmp/django.log 2>&1 &
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/api/datasets/
```

```bash
cd frontend && pnpm exec vite
```

Two browser sessions:

```bash
export AGENT_BROWSER_DEFAULT_TIMEOUT=180000
agent-browser --session dev open "http://localhost:8080/…"
```

Production needs HTTP Basic credentials, which live in `.env` as `PELICAN_PRODUCTION_URL`. Read
them out of the file at the point of use and mask the output, so they reach neither the transcript
nor a saved file:

```bash
agent-browser --session prod open \
  "$(grep -m1 '^PELICAN_PRODUCTION_URL=' .env | cut -d= -f2-)/field/91" 2>&1 \
  | sed -E 's#(://[^:]*:)[^@]*@#\1***@#g'
```

Only the session's first navigation needs them; later ones inherit the credentials. Never bake
them into a screenshot path.

## Audit the source first

Cheaper than the browser, and it finds the leaks that the browser only shows as symptoms. List
every unscoped `<style>` block, extract its top-level selectors, and check whether each selector's
classes appear in the component's own template and in anyone else's:

```python
import pathlib, re

vues = sorted(pathlib.Path("frontend/src").rglob("*.vue"))
templates = {p: (re.search(r"<template>(.*)</template>", p.read_text(), re.S) or [None, ""])[1] for p in vues}

def selectors(body):
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    out, depth, buf = [], 0, ""
    for ch in body:
        if ch == "{":
            if depth == 0: out.append(" ".join(buf.split()))
            depth, buf = depth + 1, ""
        elif ch == "}":
            depth, buf = depth - 1, ""
        elif depth == 0:
            buf += ch
    return [x for x in out if x and not x.startswith("@")]

for p in vues:
    for m in re.finditer(r"<style([^>]*)>(.*?)</style>", p.read_text(), re.S):
        if "scoped" in m.group(1):
            continue
        for sel in selectors(m.group(2)):
            names = re.findall(r"[.#]([\w-]+)", sel)
            used = [o.name for o in vues
                    if names and all(re.search(rf'class="[^"]*\b{n}\b|id="{n}"', templates[o]) for n in names)]
            print(f"{p.name:34} {sel:44} {used}")
```

Read the output for three shapes: a selector whose classes appear in **another** component's
template (the rule is leaking); the **same selector in two components** (whichever stylesheet loads
last wins); a selector matching **nothing** (dead, safe to delete). Compare the two bodies before
deduplicating — identical bodies are harmless, differing bodies are a bug waiting for a load-order
change.

## Probing

Run the same probe against both sessions and diff the numbers. Use `eval --stdin` with a quoted
heredoc; shell quoting corrupts anything with nested quotes, `!`, backticks or `$()`:

```bash
for s in dev prod; do
  echo -n "$s: "
  agent-browser --session $s eval --stdin 2>&1 <<'EVALEOF' | tail -1
(() => {
  const R = e => { const r = e.getBoundingClientRect();
    return `${Math.round(r.width)}x${Math.round(r.height)}@${Math.round(r.left)},${Math.round(r.top)}`; };
  return JSON.stringify({ bar: R(document.querySelector(".action_bar")) });
})()
EVALEOF
done
```

`eval` must return a string; wrap objects in `JSON.stringify` or you get `}` back. Read the last
line of output.

### Screenshots

Confirm both sides are the same size before comparing any number
(`JSON.stringify({w: innerWidth, h: innerHeight, dpr: devicePixelRatio})`), then:

```bash
agent-browser --session prod screenshot --full /tmp/prod-field.png
agent-browser --session dev  screenshot --full /tmp/dev-field.png
agent-browser --session dev  diff screenshot --baseline /tmp/prod-field.png
```

The mismatch percentage is not a pass or fail — Bootstrap 4 against Bootstrap 5 differs everywhere
by a few pixels. Use the diff image to **locate** regions worth measuring, then measure them.

### Geometry

Round to integers and compare. Expect systematic small differences from Bootstrap 4 → 5 — content
width 1029 vs 1035 from gutters, form rows a few px shorter — and treat anything larger as a
finding. Element height is the fastest signal that something wrapped or moved: an action bar at
92px against production's 54px means a control fell onto a second line.

### Breakpoints

`set viewport` resizes a session, so a rule that depends on a media query can be swept rather than
reasoned about:

```bash
for w in 800 1000 1199 1201 1400 1920; do
  agent-browser --session dev set viewport $w 900
  agent-browser --session dev wait 600
  echo -n "${w}px: "
  agent-browser --session dev eval 'JSON.stringify({ vw: innerWidth, pl: getComputedStyle(document.querySelector(".main_envelope")).paddingLeft })'
done
```

Sample either side of a boundary, not just round numbers: queries using `max-width: 1199.98px` and
`min-width: 1199.98px` overlap in between, and only a width in that range shows it. Restore the
viewport afterwards, or every later measurement is taken at the last width you set. Sweep derived
quantities too — the clearance between a fixed menu and the content that must avoid it is
`padding-left` minus the menu's width, and a step in it across a breakpoint is easy to see in a
sweep and hard to see by eye.

### Content and its order

Some regressions change no geometry at all. Extract the visible sequence and diff it:

```javascript
[...document.querySelectorAll("table.data_table tbody tr td:first-child")]
    .map(e => e.innerText.trim().split("\n")[0]);
```

Production's markup may differ from yours — divs where you now have tables — so write a selector
per side rather than assuming one works for both. Test the ordering against the key you expect
rather than eyeballing it:

```javascript
const alpha = [...rows].sort((a, b) => a.localeCompare(b));
rows.findIndex((r, i) => r !== alpha[i]);   // -1 means it is alphabetical
```

That is how a table that looked fine turned out to be sorted by path when it should have been in
the API's processing order. Confirm the expected order from the payload itself.

### Where a height difference comes from

Walk down from the container, depth-limited, printing box metrics until the numbers diverge:

```javascript
const walk = (e, d) => {
  const r = e.getBoundingClientRect(), c = getComputedStyle(e);
  return [`${" ".repeat(d)}${e.tagName}.${e.className.slice(0, 24)} ` +
          `${Math.round(r.width)}x${Math.round(r.height)} m=${c.marginTop}/${c.marginBottom} p=${c.paddingTop}`,
    ...(d < 3 ? [...e.children].flatMap(k => walk(k, d + 1)) : [])];
};
walk(document.querySelector(".modal_box"), 0).join("\n");
```

The level where the two sides stop matching is the level that changed.

### Whether text wrapped

Height alone is ambiguous, since a row's height often comes from a sibling. Count line boxes:

```javascript
const range = document.createRange();
range.selectNodeContents(el);
[...range.getClientRects()].length;   // 1 = one line
```

### Computed styles

For colour, spacing and font questions, compare `getComputedStyle` directly. This is how "the
button is white here and primary there" became `rgba(0,0,0,0)` vs `rgb(108,117,225)`.

```javascript
const c = getComputedStyle(el);
JSON.stringify({ bg: c.backgroundColor, color: c.color, border: c.borderColor,
                 fontSize: c.fontSize, padding: c.padding });
```

### Which rule wins

When a declaration is not applying, list every rule that matches the element and sets the property.
Output is in source order, and the last one wins at equal specificity:

```javascript
const out = [];
for (const sheet of document.styleSheets) {
  let rs; try { rs = sheet.cssRules; } catch { continue; }
  for (const r of rs) {
    if (!r.selectorText || !r.style || !r.style.width) continue;
    if (r.selectorText.split(",").some(x => { try { return el.matches(x.trim()); } catch { return false; } })) {
      out.push(`${r.selectorText} { width: ${r.style.width} }`);
    }
  }
}
```

This found `.table td.label { width: 80px }` leaking out of an unscoped `FrequencyChart` block onto
every result box in the app. Watch for the general case: **the CSS order flipped between webpack
and Vite**, so rules that lost to Bootstrap in production now win, and declarations that had never
applied became effective. When a component rule and a Bootstrap rule have equal specificity, decide
which one you want rather than relying on order.

### Hit testing

A control can look correct and be inert. Check that the element under its own centre is the element
you expect:

```javascript
const r = el.getBoundingClientRect();
JSON.stringify({
  pointerEvents: getComputedStyle(el).pointerEvents,
  hit: document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) === el,
});
```

This is how a dropdown's label turned out to carry `pointer-events: none`, leaving only its 28px
caret clickable. `agent-browser snapshot -i` lists the interactive elements, which is the quickest
check that a control is reachable at all.

### Watching a control over time

For anything that changes while a request is in flight, sample it rather than reading it once:

```javascript
const state = () => {
  const b = document.querySelector(".submit_button");
  return `disabled=${b.disabled} spinner=${!!b.querySelector("[class*=spinner]")} "${b.innerText.replace(/\s+/g, " ").trim()}"`;
};
const timeline = [state()];
// … change an input here …
for (let i = 0; i < 15; i++) {
  await new Promise(r => setTimeout(r, 500));
  timeline.push(`${(i + 1) * 500}ms ${state()}`);
}
timeline.filter((l, i, a) => i === 0 || l.replace(/^\d+ms /, "") !== a[i - 1].replace(/^\d+ms /, ""));
```

Collapsing repeats keeps the output readable. A control that never leaves its initial state is as
interesting as one that flickers: the stale count on the filter button was a spinner that never
appeared, and then a spinner that never stopped.

To see what the network is doing underneath, count requests, completions and aborts:

```javascript
const send = XMLHttpRequest.prototype.send, open_ = XMLHttpRequest.prototype.open;
window.__n = { started: 0, done: 0, aborted: 0 };
XMLHttpRequest.prototype.open = function (m, u, ...r) { this.__u = u; return open_.call(this, m, u, ...r); };
XMLHttpRequest.prototype.send = function (...r) {
  if (String(this.__u).includes("dataset-filter-items")) {
    window.__n.started++;
    this.addEventListener("loadend", () => window.__n.done++);
    this.addEventListener("abort", () => window.__n.aborted++);
  }
  return send.apply(this, r);
};
```

To expose a race, make the first request slow — throttle the network, or delay the endpoint — then
trigger a second one before it lands and check which response wins.

### Console output

Vue's diagnostics are the fastest route to a render bug, and often the only route. The catch: hooks
installed with `eval` are cleared by the reload that triggers the bug. Install them on a page that
already works, then navigate **in-app**:

```javascript
window.__e = [];
const oe = console.error, ow = console.warn;
console.error = (...a) => { window.__e.push("ERR " + a.map(x => x?.stack ? x.stack.slice(0, 400) : String(x)).join(" | ")); oe(...a); };
console.warn = (...a) => { window.__e.push("WARN " + a.map(String).join(" ").slice(0, 300)); ow(...a); };
```

then, in a second `eval`:

```javascript
history.pushState({}, "", "/dataset/91/detail/distribution.buyer");
window.dispatchEvent(new PopStateEvent("popstate"));   // vue-router listens for this
await new Promise(r => setTimeout(r, 7000));
JSON.stringify(window.__e);
```

Keep the stacks: `Unhandled error during execution of render function at <FrequencyChart>` plus
`TypeError: Cannot read properties of undefined (reading '1')` named both the component and the
line. An error thrown during render makes Vue abandon the update, so the symptom is usually
*missing or stale* markup somewhere else — do not assume the fault is where the staleness shows.

### Whether a subtree re-renders

To tell "this value is wrong" from "this subtree is stale", add a ref that changes on a timer and
print it in both places:

```javascript
const tick = ref(0);
setTimeout(() => { tick.value = 99; }, 4000);
```

Read both probes in a **single** `eval`, so they are sampled at the same instant. A subtree still
showing `0` after the timer has fired has not re-rendered. Be careful what you conclude: a probe run
against modified code only tells you about the modified code. Re-run against the committed version
before calling something a bug.

## Reproducing outside the app

Before blaming a framework, try to reproduce the structure in isolation. Two ways, in increasing
fidelity:

**Standalone, no build.** Copy the UMD builds next to an HTML file and serve the directory:

```bash
cp frontend/node_modules/vue/dist/vue.global.js .
cp frontend/node_modules/vue-router/dist/vue-router.global.js .
cp frontend/node_modules/vue-json-pretty/lib/vue-json-pretty.js .
python3 -m http.server 8099
```

Use `createWebHashHistory()`, or `python3 -m http.server` returns 404 for client-side routes.

**With the project's own toolchain.** Vite serves any HTML file in the project root, so a
`frontend/repro.html` plus `frontend/repro/*.vue` gets the real SFC compiler, the real Vue version
and `<script setup>` semantics, with no backend. Delete both when finished.

A failed reproduction is informative but weak evidence: it narrows what the cause *is not*. Build
the layers up one at a time — compiler, router, store, third-party components, wrapper components —
and note that a component throwing in the slot you are *not* watching is easy to leave out.

## Gotchas

- **A worktree-isolated session cannot run `agent-browser eval` at all** — the harness refuses any
  command that runs a string through eval, in both the quoted and `--stdin` forms, because it
  cannot verify the string stays inside the worktree. Nearly every probe above depends on it. Work
  from the main checkout, or leave the worktree first (`ExitWorktree` with `keep`): the directory
  and branch stay on disk, so the dev server still runs from there. `open`, `snapshot`,
  `screenshot`, `diff`, `find` and `get` are unaffected, which is enough for a smoke test but not
  for measuring anything.
- `agent-browser open` is a full page load, so it clears anything installed with `eval`.
- The agent-browser daemon returns `Resource temporarily unavailable` when busy. Re-run, or use a
  separate `--session`.
- Playwright driven directly is steadier than the daemon for clipboard work, which additionally
  needs a headed browser.
- Production is Bootstrap 4 and BootstrapVue; local is Bootstrap 5 and bootstrap-vue-next. Expect
  renamed classes (`text-right` → `text-end`, `text-muted` → `text-body-secondary`),
  `.form-control` losing its fixed height, `.col-*` setting `width` rather than `flex-basis`, and
  `.row > *` gaining `width: 100%`. `.table` also moves from styling cells by descent to
  `.table > :not(caption) > * > *`, which needs a row group — and Vue builds the DOM rather than
  parsing it, so a `<table>` written without a `<tbody>` never gets the implicit one the HTML parser
  would have inserted, and loses its borders.
- Bootstrap 5 labels a background in black unless it contrasts with white at 4.5:1, so themed
  buttons can change text colour. `$min-contrast-ratio` is the knob.
- Check what an element is allowed to contain before wrapping content in it. `.form-text` belongs on
  a `div`, not a `small`, which accepts phrasing content and so cannot hold a paragraph. Nothing
  warns about it, and the browser renders it anyway.
