---
name: gpuix
description: Build native GPU-accelerated desktop apps with GPUIX — React (or Solid) rendered by GPUI, Zed's GPU UI framework, via TypeScript and Bun. No Electron, no web view, no DOM. Use this whenever the work involves GPUIX or @gpuix/react (jsxImportSource, render(), motion.div, virtual-list, createTestRoot), GPUI, or writing a real desktop app in React/TypeScript where the user wants native windows, GPU rendering, and a compiled binary. Also use it when someone is already using GPUIX and something is wrong in ways that look like React bugs but are not — text that renders black, a list that janks, a scroll that steals gestures, an inner scroller that won't scroll, hover styles that don't apply, a window that opens twice on save, a spinner on a click. Read this before writing GPUIX code, not after it fails, because most of the painful behaviours here are silent and look like framework bugs rather than API misuse.
---

# GPUIX — building native desktop apps with React

GPUIX paints a React tree with **GPUI**, Zed's GPU UI framework. You write
`useState` and JSX in TypeScript; it lays out with flexbox and renders through
Metal, DirectX, or Vulkan. The result is a real native binary with a real
window — not a web view in a wrapper.

GPUI is **immediate-mode**: it rebuilds an element tree every frame. GPUIX
embraces that rather than fighting it. React computes a minimal set of
mutations, sends them across an atomic `applyBatch()` call, and a Rust-side
`RetainedTree` reconciles them into GPUI elements each frame. Only changed
elements cross the FFI boundary.

This is the React path for native desktop apps. The Solid path is real and
documented (`references/solid.md`) but is a separate adapter with its own
setup; unless asked for it, build React.

## The shortest path to a correct app

Three things are required and two of them fail silently if omitted.

```bash
bunx @gpuix/cli new my-app && cd my-app && bun run dev
```

That command downloads the official `example-app/` and installs dependencies —
no repository clone, no Rust toolchain, no native build. Copy it as your
starting point rather than wiring a project from scratch.

Building by hand instead:

```bash
bun add --exact @gpuix/react @gpuix/native react
bun add -d @types/react typescript
```

`tsconfig.json` — **`jsxImportSource` is required**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "jsxImportSource": "@gpuix/react",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true
  }
}
```

Without it TypeScript resolves JSX against DOM types, so `<virtual-list>`,
`<markdown>`, `<code>`, and `style.hover` all fail to typecheck while the
runtime would have worked.

The entry file ends with `render()`:

```tsx
import { useState } from "react";
import { render } from "@gpuix/react";

function App() {
  const [count, setCount] = useState(0);
  return (
    <div style={{ padding: 24, backgroundColor: "#1a1a1a", height: "100%" }}>
      <div
        onClick={() => setCount((c) => c + 1)}
        style={{
          padding: 12,
          borderRadius: 8,
          cursor: "pointer",
          backgroundColor: "#232323",
          hover: { backgroundColor: "#2c2c2c" },
        }}
      >
        <text style={{ color: "#e2e2e2" }}>Count: {count}</text>
      </div>
    </div>
  );
}

render(<App />, { title: "My App", width: 800, height: 600 });
```

Run it with **`bun --hot`**, not plain `bun`:

```bash
bun --hot app.tsx
```

Ship a single binary with no runtime dependency:

```bash
bun build --compile app.tsx --outfile dist/app
```

## Traps

These fail quietly. Each one has cost someone an afternoon, and most look like
a React or GPUI bug rather than a mistake in how the API is being called. When
something behaves impossibly, look here before debugging your own code.

### Setup

- **`jsxImportSource` must be `"@gpuix/react"`.** Miss it and you get DOM types:
  `<virtual-list>`, `<markdown>`, `<code>`, and `style.hover` stop typechecking.
- **Pin `@gpuix/react` and `@gpuix/native` to the same exact version.** GPUIX is
  pre-1.0. The adapter pulls `@gpuix/native` with a _version range_, so that
  range can install a newer native binary under an older adapter. Add both as
  direct dependencies and upgrade them together. This is the single most
  common source of "it worked yesterday" breakage.
- **No Rust toolchain is needed to build an app.** The published packages ship
  the renderer. Only working _on GPUIX_ requires the submodule and native
  build.

### "It renders but looks wrong"

- **Give every `<text>` an explicit `color`.** GPUI does **not** inherit `color`
  from a parent, so text with no color paints black and disappears on a dark
  surface. This is not a styling preference; it is invisible output.
- **`hover` is a GPUI style, not a CSS pseudo-class.** `style.hover` is a
  sibling key inside `style`, applied natively on pointer enter/leave. There is
  no `&:hover` selector.
- **Style props are camelCase React-style; there is no CSS shorthand engine.**
  No `padding: '12px 16px'`. No `margin: 0 auto`. Flexbox properties only —
  Taffy lays out, not the browser.
- **Controls are unstyled primitives, not a component library.** There is no
  `<Select options={...} />`. Each primitive lives behind its own namespace
  entry point (`@gpuix/react/select`, `/combobox`, `/tooltip`, `/floating`) and
  exports parts you compose and style yourself, the way Radix primitives work in
  shadcn. Build a local `components/ui/select.tsx` and import that.
- **A clickable `<div>` is not a button to a screen reader.** A node enters the
  macOS AX tree only when it has **both** a GPUI id and a `role`. Add
  `role="button"` plus `aria-label`. `<text>`, `<input>`, `<textarea>`, and
  `<img>` have sensible defaults; plain divs do not.

### The dev loop

- **Use `bun --hot`. Plain `bun` opens a second process and window on save.**
  With `--hot`, `render()` remounts React on the _same_ window: the window, GPU
  device, `.node` addon, and GPUI scroll physics all survive. `useState`, focus,
  and React handlers do not — this is a **remount**, not React Refresh, and
  getting hook state to survive needs a Bun runtime transform that does not
  exist yet (`bun build --react-fast-refresh` only).
- **Call `render()` in the entry file. Never `createRenderer()` + `init()`.**
  `bun --hot` re-runs the whole entry on save, so a second `init()` builds a
  second host and opens a second window. `render()` is idempotent: the first
  call owns the window, later calls only remount React. `createRenderer()`,
  `createRoot()`, and `startFrameLoop()` stay public for tests and custom hosts.
- **One renderer drives one root.** A renderer owns one window, one native root,
  and one event map, so `createRoot()` throws if that renderer already has a
  mounted root. `unmount()` the first before creating another.
- **Native `.node` edits need a rebuild.** Native modules cannot be unloaded,
  so there is no hot reload for the Rust side. `bun run dev` rebuilds and
  restarts.
- **Never drive `tick()` from a `setImmediate` loop on macOS.** That spins at
  tens of thousands of ticks per second and burns **73% CPU on a completely
  idle app**, versus 1% when paced. Leave the frame loop alone unless you are
  deliberately driving a custom host.
- **A runtime throw does not freeze the window or kill the process.** The window
  shows the stack and a Reload button. So "the app froze" and "the handler
  threw" look the same from outside — check the overlay before assuming a hang.

### Interaction and layout

- **Nested scrolling is not supported.** GPUI gives the inner and outer hitboxes
  the same wheel event, so an inner `overflow: "scroll"`, `<virtual-list>`, or
  `<diff>` **steals the gesture** and the parent never scrolls. Keep long inner
  content in the parent, or collapse it behind an expandable. Horizontal
  `overflowX: "scroll"` is the exception — but the wide child must not shrink
  (`flexShrink: 0` or a definite width), or the scroller collapses.
- **A plain `overflow: "scroll"` container builds every child.** Fine for small
  lists; use `<virtual-list>` when the collection can grow, or scrolling will
  cost you frames exactly when you can least afford it.
- **A `motion.div` `exit` only fires inside `<AnimatePresence>`,** and every
  child that can leave needs a unique `key`. Without the wrapper, React destroys
  the node on the same commit. `initial={false}` skips the enter animation when
  an element should mount at its first `animate` target.
- **`motion.div` accepts numeric targets only** — `width`, `height`, `top`,
  `right`, `bottom`, `left`, `opacity`, `borderRadius`. Springs, keyframes,
  variants, and shared-layout animations are not available yet.
- **Animate an outer clipping container** to collapse a sidebar, and keep the
  inner element at a fixed width. Animating the inner element reflows its text
  every frame.
- **`flushSync` flushes React only, not GPUI.** When it returns the native
  retained tree is current, including styles and text — but layout and paint
  still happen on the next frame, exactly like the browser after a DOM mutation.
  In a test, call `renderer.flush()` to see pixels.
- **Do not bind `focusNext()` in both an element `onKeyDown` and a renderer
  `onKeyDown`.** Both move focus and the window listener cannot cancel the
  native event, so Tab jumps twice. Renderer keyboard callbacks fire only for
  raw keys that no GPUI action already consumed.

### Window and platform

- **`focus: false` and `show: false` are ignored on Linux.** The window opens
  focused. macOS and Windows honor both. `focus: false` is what keeps a coding
  agent's screenshot-and-click loop from stealing your window every iteration —
  worth setting, but do not expect it to work on Linux.
- **`appName` does not set the application menu's title.** macOS takes that from
  the executable, so `bun app.tsx` shows `bun` during development and a
  `bun build --compile` binary shows its own filename. Only a real `.app` bundle
  changes it. `appName` reaches the items _inside_ the menu.
- **There is deliberately no Edit menu.** A menu key equivalent is consumed by
  AppKit before the window sees the event, so an Edit menu carrying ⌘C would
  steal the keystroke from text selection and from `<input>`. Do not "fix" this
  by adding one.
- **`promptForPaths()` returns OS paths, so it rejects in the browser.** Windows
  also cannot distinguish cancellation from other file-dialog errors, so both
  resolve `null`.

### Shipping

- **Packaging does not turn on updates.** Auto-update is a separate
  `checkUpdate()` call from `@gpuix/native`, and it needs a **public** GitHub
  repo or the API returns 404.
- **`downloadAndInstall()` replaces the files but does not relaunch.** Quit after
  it returns or the next start uses the old app.
- **The macOS updater wants the `.app.tar.gz`**, not the `.app` and not a
  `.dmg` — packager only tars when it signs. Linux and Windows artifact names
  use the _binary stem_, not `productName`. NSIS arch is `x64`, not `x86_64`.
- **`cargo packager` builds only the host OS.** Run it on macOS, Linux, and
  Windows. `--release` is the packager profile, not `cargo build --release`.
- **`cargo-packager` rejects a 1024x1024 PNG** with `No matching IconType`. Build
  an `.icns` first.
- **On the Hermes path, the `.node` sidecar must be listed as a second
  _binary_, not a resource.** `dlopen` looks in `Contents/MacOS`; resources go
  to `Contents/Resources`.
- **Browser builds need `Cross-Origin-Opener-Policy: same-origin` and
  `Cross-Origin-Embedder-Policy: require-corp` on the top-level document.** The
  Wasm uses shared memory. `require-corp` then constrains every cross-origin
  subresource, so serve the JS and Wasm from the same origin.

## What to read, and when

Load one file per task. They are verbatim slices of the upstream docs with a
table of contents at the top of each.

| You are doing this                                                                                                                                                                                   | Read                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Creating a project, running it, packaging, icons, auto-update, signing, the example apps, package layout, building GPUIX itself                                                                      | `references/01-quickstart-and-ship.md`       |
| Window options, `titlebarTransparent` / `windowBackground`, the macOS menu bar, background launch, driving the app from a coding agent, window controls, file picker, frame-time overlay, hot reload | `references/02-window-and-dev-loop.md`       |
| Scroll containers, the nested-scroll rule, `<virtual-list>`, programmatic scrolling                                                                                                                  | `references/03-layout-and-lists.md`          |
| Native `<input>` / `<textarea>`, text selection, highlighting and search, `<code>` / `<diff>` / `<markdown>`                                                                                         | `references/04-text-and-input.md`            |
| Accessibility and ARIA mapping, focus and keyboard navigation, Select / Combobox / Tooltip / FloatingLayer, `motion.div` and `AnimatePresence`                                                       | `references/05-interaction-and-animation.md` |
| Which elements, events, and style props exist; images, SVG icons, and the current build status                                                                                                       | `references/06-api-surface.md`               |
| The mutation protocol, event flow, window observers, text search internals, the automation client, `TestRenderer`, working on the Rust side                                                          | `references/07-architecture-and-testing.md`  |
| Solid 1 instead of React                                                                                                                                                                             | `references/solid.md`                        |
| A smaller binary without Bun (`hermes-node`, 12 MB + 22 MB sidecar)                                                                                                                                  | `references/hermes.md`                       |
| Whether a behaviour is new, changed, or broken                                                                                                                                                       | `references/changelog.md`                    |

`06-api-surface.md` is the lookup file. When you are not sure whether a prop or
element exists, read it before writing the call — inventing a plausible API is
the most common way to get stuck here.

## Checking your work

- **Types first.** `bun run typecheck`. The `jsxImportSource` mistake and any
  invented prop surface here immediately.
- **Screenshot it.** Rendering is not crashing. Use the automation client
  (`launch()` from `@gpuix/react/automation`) or `createTestRoot()` from
  `@gpuix/react/testing` — the latter opens **no window at all**, so it cannot
  steal focus and keyboard input works. `click()` and `screenshot()` do not
  need window focus either.
- **Test out of spec.** A GPU-backed renderer is only worth having if you check
  the awkward states: empty data, long data, a slow dependency, focus taken away
  mid-interaction.
- **Watch frame time, not just correctness.** `render(<App />, { debugFrameOverlay: 'full' })`
  paints draw-time stats into the window. The overlay's `p90Ms` is the 10% line
  and `p99Ms` the 1% line — those are the tail that jank actually comes from.

## Boundaries worth knowing

From `references/06-api-surface.md`, these are **not built** — do not design
around them:

- `<canvas>` and custom drawing
- Multiple windows
- App-declared menus and menu callbacks
- React Refresh under `bun --hot` (hook state resets on save)
- Hot reload of the native `.node` addon

If the user's design needs one of these, say so up front rather than
discovering it at build time. GPUIX is pre-1.0 and moves fast — when something
seems impossible, check `references/changelog.md` before concluding it is not
there.
