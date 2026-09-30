> Agent-readable docs index: /llms.txt. Full docs in one file: /llms-full.txt. Download /docs.zip to grep all markdown files locally.

---

title: "Changelog"
description: "Release notes for Changelog."
mode: "center"
---

import _ChangelogIntro from './changelog/intro.mdx'

<Aside full>
  <Note>
    This changelog is generated automatically from the [GitHub releases](https://github.com/remorses/gpuix/releases) page.
  </Note>
</Aside>

Every entry below is a **GitHub release** of `@gpuix/react` and `@gpuix/native`.
Both packages are published together by CI, so a version number always names the
same commit on both sides of the bridge.

Each release also carries a **prebuilt example app** (`example-chat-<target>`)
for macOS, Linux, and Windows. Download it from the release page to see the chat
example run on the GPU without installing Rust.

<Update id={"@gpuix/solid@0.10.0"} label={"Sep 23, 2026"}>

## @gpuix/solid\@0.10.0

First release of `@gpuix/solid`, the official Solid 1 renderer for GPUIX. Solid apps run with normal Bun commands and a preload. No Vite, no wrapper CLI.

```bash
bun add --exact @gpuix/solid @gpuix/native solid-js
```

```json
{
  "compilerOptions": {
    "jsx": "preserve",
    "jsxImportSource": "@gpuix/solid"
  }
}
```

```toml
# bunfig.toml
preload = ["@gpuix/solid/preload"]
```

```tsx
import { createSignal } from "solid-js";
import { render } from "@gpuix/solid";

const [count, setCount] = createSignal(0);

render(() => (
  <div onClick={() => setCount((value) => value + 1)}>
    <text>Count: {count()}</text>
  </div>
));
```

**What ships**

1. Native `motion` and `AnimatePresence`, with the same API as `@gpuix/react`
2. Headless `Select`, `Combobox`, and `Tooltip`
3. Shared testing and automation from `@gpuix/native/testing` and `@gpuix/native/automation`
4. Solid JSX declarations for every GPUIX element
5. `@gpuix/solid/preload` for `bun app.tsx`, and `@gpuix/solid/bun-plugin` for production `Bun.build` calls:

```ts
import solidPlugin from "@gpuix/solid/bun-plugin";

await Bun.build({
  entrypoints: ["./app.tsx"],
  target: "bun",
  plugins: [solidPlugin],
});
```

Pin `@gpuix/solid` and `@gpuix/native` to the same exact version.

Empty text nodes now take no layout space. Solid creates an empty placeholder for every dynamic hole (`<Show>`, `<For>`, `{cond && <x/>}`), and those no longer stretch flex columns.

The rest of 0.10.0 (live image uploads, `scrollIntoView`, window controls, `promptForPaths`, caret and paste fixes) is in the [`@gpuix/react@0.10.0` release](https://github.com/remorses/gpuix/releases/tag/%40gpuix%2Freact%400.10.0). Those native features work from Solid too.
</Update>

<Update id={"@gpuix/react@0.10.0"} label={"Sep 21, 2026"}>

## @gpuix/react\@0.10.0

1. **Framework-neutral runtime moves into `@gpuix/native`.** Host contracts, testing, and automation now live in `@gpuix/native/host`, `@gpuix/native/testing`, and `@gpuix/native/automation`. React keeps its current public imports as adapters and re-exports, so existing React code does not change. The native package now exposes an ESM loader by default; its explicit CommonJS condition remains for the documented Hermes runtime.

   This split is what powers the new [`@gpuix/solid@0.10.0`](https://github.com/remorses/gpuix/releases/tag/%40gpuix%2Fsolid%400.10.0) renderer, released separately.

2. **Add exit animations for `motion.div`** through an `AnimatePresence` API shaped like Motion for React.

   ```tsx
   import { AnimatePresence, motion } from "@gpuix/react";

   function Toast({ show }: { show: boolean }) {
     return (
       <AnimatePresence>
         {show ? (
           <motion.div
             key="toast"
             initial={{ opacity: 0 }}
             animate={{ opacity: 1 }}
             exit={{ opacity: 0 }}
             transition={{ duration: 0.2 }}
           >
             <text>Saved</text>
           </motion.div>
         ) : null}
       </AnimatePresence>
     );
   }
   ```

   React keeps the leaving node mounted. Native motion tweens to `exit`, then `motionComplete` lets `AnimatePresence` unmount it. Without `AnimatePresence`, unmount is still immediate. Give each leaving child a unique `key`.

   Completion stays tied to the target that started it, including no-op targets, and offscreen virtual-list rows finish without being painted. A partial exit target also keeps animated properties it does not replace.

3. **Add live image uploads and `scrollIntoView` on host refs.** `<img>` refs can push image bytes without a data URL or JSON mutation:

   ```tsx
   const img = useRef<ImgInstance>(null);

   useLayoutEffect(() => {
     img.current?.setImage(pngBuffer);
     img.current?.setImagePixels(800, 80, rgbaBytes);
   }, [pngBuffer, rgbaBytes]);

   return <img ref={img} style={{ width: 800, height: 80 }} />;
   ```

   `setImage` takes encoded PNG, JPEG, WebP, GIF, SVG, BMP, TIFF, ICO, or Netpbm. `setImagePixels` takes packed RGBA. Prefer pixels for a live frame. There is no density argument. Upload a 2x bitmap into a 1x layout box on retina. Alpha is straight, not premultiplied. A later React `src` change overwrites the pixels.

   Every host ref now has `scrollIntoView()`, which scrolls the nearest overflow parent or `<virtual-list>` until that node is visible. On a windowed list it uses the logical item index, not the mounted child index.

4. **Add native desktop window controls** to the renderer.

   ```tsx
   const renderer = useGpuixRequired();

   renderer.minimizeWindow?.();
   renderer.zoomWindow?.();
   renderer.toggleFullscreen?.();
   ```

   The methods forward to GPUI's platform window on macOS, Windows, Linux, and FreeBSD. They are not available in the browser renderer.

5. **Add `renderer.promptForPaths()`** for opening the operating system's file picker.

   ```tsx
   const paths = await renderer.promptForPaths({
     files: true,
     multiple: true,
     prompt: "Attach",
   });
   ```

   The promise resolves with absolute paths, resolves with `null` on cancellation, and rejects for invalid options, platform failures, or browsers where operating-system paths are unavailable. Custom renderers can omit the optional capability.

   The current Windows GPUI backend reports `IFileDialog::Show` errors as cancellation. Those cases also resolve with `null` until GPUI distinguishes the system error code.

6. **Draw the `<input>` and `<textarea>` caret at line height**, like Chrome.

   A composer with `fontSize: 14` and `lineHeight: 20` now paints a 20px bar instead of a 14px em-square bar. Extra leading stretches the caret with the row.

7. **Let `Cmd+V` and `Ctrl+V` reach `onKeyDown` when the clipboard has no text.**

   Text still pastes natively, including text accompanied by an image. Applications can now handle image-only and file clipboard contents instead of losing the paste shortcut or inserting a copied file path as text.

8. **Keep uniformly rounded and per-corner rounded Select, Combobox, and Tooltip content rounded** through the complete deferred overlay surface. The anchored fallback background no longer appears as square corners behind a rounded popup.

   The outer surface now also owns visibility and opacity, including hover and active refinements, so its fallback fill follows the content without multiplying opacity. `pointerEvents: "none"` disables the anchored occluder.

Fixes [https://github.com/remorses/gpuix/issues/68](https://github.com/remorses/gpuix/issues/68)
</Update>

<Update id={"@gpuix/react@0.9.0"} label={"Sep 16, 2026"}>

## @gpuix/react\@0.9.0

1. **Add a window-level `onSelectionChange` callback** so React apps can react when the text selection changes.

   Pass it to `render()` or `createRoot()`, the same way as `onKeyDown`. The payload is a normal `EventPayload`. `value` is the joined selected text, or omitted when the selection is empty.

   ```tsx
   render(<App />, {
     onSelectionChange(event) {
       setCopied(event.value ?? "");
     },
   });
   ```

   The event fires once per real change, including a clear. An unchanged frame does not fire.

2. **Fix a live-window panic on ordinary mouse clicks and text-selection drags.** A physical left click aborted the app with `cannot update GpuixView while it is already being updated`. AppKit dispatches the event with the root view already leased, and GPUIX then nested-updated that same view from the text-selection mouse-up listener.

   A tap now skips drag-end cleanup when no drag was active. Real selection-drag move and end work run after the current GPUI effect cycle, so the root lease is released first.

3. **Pin `@gpuix/react` and `@gpuix/native` to the same exact version.** GPUIX is still pre-1.0. A new release can break either package. `@gpuix/react` depends on `@gpuix/native` with a version range, so that range can install a newer native binary under an older React package. Add both as direct dependencies and upgrade them together.

   ```bash
   bun add --exact @gpuix/react @gpuix/native react
   ```

Fixes [https://github.com/remorses/gpuix/issues/38](https://github.com/remorses/gpuix/issues/38)
</Update>

<Update id={"@gpuix/react@0.8.0"} label={"Sep 14, 2026"}>

## @gpuix/react\@0.8.0

1. **Expose GPUI accessibility through React `role` and `aria-*` props.** VoiceOver, Accessibility Inspector, and other AX clients can now see labelled controls instead of an empty window. A node is in the platform tree only with both a GPUI id and a role.

   ```tsx
   <div
     role="button"
     aria-label="Delete note"
     aria-id="notes.delete"
     onClick={remove}
   >
     Delete
   </div>
   ```

   Prop names match React DOM (`aria-label`, not `ariaLabel`). Role values are ARIA tokens (`"button"`, `"heading"`). `"none"` / `"presentation"` produce no node. `<text>` defaults to `Label`, `<input>` to `TextInput`, `<textarea>` to `MultilineTextInput`, `<img>` to `Image` with `alt`. `onClick` registers AccessKit Click, so VoiceOver Press fires the same JS handler. Browser / wasm has no AccessKit adapter; these props are no-ops there.

2. **Let component libraries wrap Select without rewriting children.** Select follows Base UI’s split between Root label data and mounted Item interaction data. `items` on Root is optional. It is a label lookup for `SelectValue` while the menu is closed. Keyboard nav and clicks read the mounted `SelectItem` children, so a styled wrapper around `Item` works. Without `items`, `SelectValue` shows the raw value. `disabled` lives on `SelectItem`.

   ```tsx
   const models = [
     { value: 'sonnet', label: 'Sonnet' },
     { value: 'opus', label: 'Opus', disabled: true },
   ]

   <Select items={models} value={model} onValueChange={setModel}>
     <SelectTrigger>
       <SelectValue placeholder="Select a model" />
     </SelectTrigger>
     <SelectContent>
       {models.map((item) => (
         <SelectItem key={item.value} value={item.value}>
           {item.label}
         </SelectItem>
       ))}
     </SelectContent>
   </Select>
   ```

   GPUI has no bubbling. Use `asChild` on `SelectItem` and `ComboboxItem` when a styled row paints the fill, so that row becomes the real hit target:

   ```tsx
   <SelectItem value="opus" asChild>
     <MenuRow>Claude Opus 4.6</MenuRow>
   </SelectItem>
   ```

   The child must forward its ref and host props. `@gpuix/react` now exports `Props`, `GpuixTheme`, `GpuixMetrics`, `InputProps`, `AnchoredProps`, and the other host prop types. Import `FloatingLayer` and `renderSlot` from `@gpuix/react/floating`. `getElementBounds(id)` is on the live renderer and returns `{ x, y, width, height }`, or `null`. `getFocusedElementId()`, `focusNextWithin(id)`, and `focusPreviousWithin(id)` walk GPUI's painted tab map.

3. **Add `onFileDrop` for Finder and OS file drops.** Put the listener on the element that should receive the drop. GPUI hit-tests the pointer and delivers the paths to that node.

   ```tsx
   <div
     onFileDrop={(event) => openFiles(event.paths ?? [])}
     style={{ width: 400, height: 300 }}
   >
     <text>Drop files here</text>
   </div>
   ```

   `event.paths` is `string[]`: absolute Unicode filesystem paths. Works on `div`, `text`, `img`, `svg`, `input`, `textarea`, `code`, `markdown`, `diff`, and `anchored`. `<virtual-list>` does not take this event; wrap it in a `div`. Desktop only.

4. **Add `checkUpdate()` on `@gpuix/native` so a packaged app can update itself from GitHub Releases.** HTTP uses the same `reqwest_client` as `<img>`.

   ```tsx
   import { checkUpdate } from "@gpuix/native";

   const update = await checkUpdate("0.1.0", {
     endpoints: ["https://github.com/OWNER/REPO/releases/latest"],
     pubkey: "<public key from cargo packager signer generate>",
   });
   if (update) await update.downloadAndInstall();
   ```

   Create the GitHub release first. On each OS run `cargo packager --release --config packager.json` with `CARGO_PACKAGER_SIGN_PRIVATE_KEY` set, then `gh release upload` the bundle and its `.sig`. `downloadAndInstall()` replaces the packaged files and does not relaunch. Desktop only.

5. **Open a window as a Wayland `wlr-layer-shell` surface via `WindowOptions.layerShell`.** `render(node, { layerShell })` opens a compositor-anchored bar, dock, notification overlay, or wallpaper instead of a normal floating window.

   ```tsx
   render(<Bar />, {
     appId: "my-panel",
     height: 34,
     windowBackground: "opaque",
     focus: false,
     layerShell: {
       namespace: "my-panel",
       layer: "top",
       anchor: ["top", "left", "right"],
       exclusiveZone: 34,
       keyboardInteractivity: "none",
     },
   });
   ```

   Linux/Wayland only; ignored on macOS and Windows. `appId` also sets the Wayland `app_id` / X11 `WM_CLASS` on a normal window.

   Thanks @KiteShell for [https://github.com/remorses/gpuix/pull/64](https://github.com/remorses/gpuix/pull/64)

6. **Add http(s) `src` support to `<img>`.** GPUI fetches the URL in the background and paints when decode finishes. Pass both `width` and `height` so the box does not jump after load.

   ```tsx
   <img
     src="https://example.com/avatar.png"
     objectFit="cover"
     style={{ width: 48, height: 48, borderRadius: 24 }}
   />
   ```

7. **Add `textDecoration` style** with `"underline"`, `"line-through"`, and `"none"`:

   ```tsx
   <text style={{ color: "#3b82f6", textDecoration: "underline" }}>
     Learn more
   </text>
   ```

8. **Make Enter insert a newline in `<textarea>` unless `onSubmit` is set.** `<textarea>`: Enter and Shift+Enter insert a newline. `<textarea onSubmit={send}>`: Enter emits `onSubmit`; Shift+Enter still inserts a newline. `<input>`: Enter still emits `onSubmit`.

9. **`<input>` and `<textarea>` size their rows from `style.fontSize` and `style.lineHeight`.** Without an explicit `lineHeight`, the row follows GPUI's default leading. Single-line `<input>` now vertically centers text, clips to `borderRadius`, and draws the caret at about 75% of `fontSize`.

10. **Keep the macOS window alive after a JavaScript runtime error, and show a stack overlay with Reload.** `render()` catches `tick()` errors, native event callbacks, `uncaughtException`, and `unhandledRejection`. **Reload** remounts the last tree.

11. **Keep click, keyboard, and other event handlers active after `bun --hot` remounts an app on its existing native window.**

12. **Deliver `onClick` from primary-button mouse-up** for retained and custom native elements so embedded macOS windows receive clicks reliably.

13. **Keep Bun responsive while GPUIX pumps embedded AppKit events on macOS.** `GpuixRenderer.tick()` now drains only native work that is ready.

14. **Prevent live-app mouse automation from aborting the GPUI process** when a locator clicks, hovers, wheels, or drags.

15. **Keep an element's style when React hides it.** `hideInstance` now keeps the existing style and only adds `visibility: "hidden"`.

16. **Stop the browser chat example from dying before the WebGPU window opens.** Window-key listeners and `focusElement()` calls made while the asynchronous WebGPU window opens are queued until the window exists.

17. **Document how to ship a GPUIX React app on [hermes-node](https://github.com/tmikov/hermes-node).** The guide is at `website/src/guides/hermes.mdx`.

Fixes [https://github.com/remorses/gpuix/issues/37](https://github.com/remorses/gpuix/issues/37)
Fixes [https://github.com/remorses/gpuix/issues/38](https://github.com/remorses/gpuix/issues/38)
Fixes [https://github.com/remorses/gpuix/issues/39](https://github.com/remorses/gpuix/issues/39)
Fixes [https://github.com/remorses/gpuix/issues/41](https://github.com/remorses/gpuix/issues/41)
Fixes [https://github.com/remorses/gpuix/issues/46](https://github.com/remorses/gpuix/issues/46)
Fixes [https://github.com/remorses/gpuix/issues/47](https://github.com/remorses/gpuix/issues/47)
Fixes [https://github.com/remorses/gpuix/issues/59](https://github.com/remorses/gpuix/issues/59)
Fixes [https://github.com/remorses/gpuix/issues/63](https://github.com/remorses/gpuix/issues/63)
</Update>

<Update id={"@gpuix/react@0.7.0"} label={"Sep 1, 2026"}>

## @gpuix/react\@0.7.0

1. **Add native two-stop linear gradients to `style.background`.** Gradients use GPUI's GPU shaders on every renderer. Angles follow CSS direction, stop positions range from `0` to `1`, rounded corners work as expected, and `hover` or `active` can replace the gradient.

   ```tsx
   <div
     style={{
       background: {
         type: "linear-gradient",
         angle: 90,
         stops: [
           { color: "#7c3aed", position: 0 },
           { color: "#06b6d4", position: 1 },
         ],
         colorSpace: "oklab",
       },
       borderRadius: 12,
     }}
   />
   ```

   `colorSpace` accepts `"srgb"` or `"oklab"` and defaults to `"srgb"`. GPUI does not support radial, conic, repeating, or gradients with more than two stops.

2. **Add data URL sources to `<img>`.** Images created or loaded in memory can now render without a temporary file:

   ```tsx
   const src = `data:image/png;base64,${Buffer.from(pngBytes).toString('base64')}`

   <img src={src} style={{ width: 240, height: 140 }} />
   ```

   Base64 and percent-encoded data URLs support PNG, JPEG, WebP, GIF, SVG, BMP, TIFF, ICO, and Netpbm images. Filesystem paths continue to work.

3. **Applications now own Tab key behavior.** GPUIX no longer binds Tab or Shift+Tab to focus traversal. Both keys reach normal element keyboard handlers and the renderer-level `onKeyDown` callback, so terminals and editors can process them directly.

   Applications that want focus traversal can call the direct GPUI wrappers from the renderer callback:

   ```tsx
   render(<App />, {
     onKeyDown(event, renderer) {
       if (event.key !== "tab") return;
       if (event.modifiers?.shift) renderer.focusPrevious?.();
       else renderer.focusNext?.();
     },
   });
   ```

   `render()` also accepts `onKeyUp`. Element callbacks run before renderer callbacks for raw keys that no GPUI action consumed. Renderer callbacks observe events but cannot cancel native propagation.

4. **Export `TestGpuixRenderer` consistently on every platform.** macOS and Windows builds with test support construct the GPU renderer. Linux and other builds without test support now throw a clear availability error instead of `TypeError: TestGpuixRenderer is not a constructor`.

   ```ts
   import { TestGpuixRenderer, hasTestGpuixRenderer } from "@gpuix/native";

   if (hasTestGpuixRenderer()) {
     const renderer = new TestGpuixRenderer();
   }
   ```

   `@gpuix/react/testing` exposes the matching `hasNativeTestRenderer` guard. `GpuixRenderer` is unchanged and continues to work on Linux.

5. **Fix blurry Windows text above 100% display scaling.** The native UI thread requests Per-Monitor V2 DPI awareness before GPUI creates a window, so Windows no longer bitmap-stretches GPUIX apps hosted by Node or Bun. Processes that already have Per-Monitor V2 awareness keep their existing configuration.

6. **Quit after the last window closes on Windows and Linux.** Closing the final GPUIX window now ends the Node or Bun process, matching macOS. `tick()` reports when the native UI thread has ended, and `render()` exits on that signal.

7. **Add a macOS frosted-glass window example.** It combines GPUI's native vibrancy backdrop with a transparent titlebar and translucent React surfaces:

   ```tsx
   render(<App />, {
     titlebarTransparent: true,
     windowBackground: "blurred",
   });
   ```

   Run it from `examples/` with `bun run blurred-window`.

Fixes [https://github.com/remorses/gpuix/issues/30](https://github.com/remorses/gpuix/issues/30)
Fixes [https://github.com/remorses/gpuix/issues/31](https://github.com/remorses/gpuix/issues/31)
Fixes [https://github.com/remorses/gpuix/issues/32](https://github.com/remorses/gpuix/issues/32)
Fixes [https://github.com/remorses/gpuix/issues/35](https://github.com/remorses/gpuix/issues/35)
Fixes [https://github.com/remorses/gpuix/issues/36](https://github.com/remorses/gpuix/issues/36)
</Update>

<Update id={"@gpuix/react@0.6.0"} label={"Aug 29, 2026"}>

## @gpuix/react\@0.6.0

1. **Every interactive surface now has a stable GPUI identity.** `hover` and `active` work on `<text>`, `<input>`, `<textarea>`, `<code>`, `<markdown>`, `<diff>`, `<img>`, `<svg>`, and `<anchored>`, not only `<div>`. `<text>` also receives its declared click, mouse, keyboard, focus, and pointer-capture events.

   ```tsx
   <text style={{ padding: 8, hover: { color: '#f38ba8' } }} onClick={select}>
     {label}
   </text>

   <img src={avatar} onClick={openProfile} />
   <anchored side="bottom" onMouseLeave={close}>{items}</anchored>
   ```

   `<img>`, `<svg>`, and `<anchored>` now report painted bounds to automation. Animated GIFs retain frame state. An `active` style no longer needs an unrelated click handler. A filled `<text>` takes mouse hits like HTML; set `pointerEvents: 'none'` to keep the old pass-through. `createRoot(renderer)` throws if that renderer already has a mounted root. Removed text nodes are freed.

2. **Background window launch and live keyboard automation.** `render()` adds `focus` and `show`. `focus: false` opens behind the current app. `show: false` creates the live tree with no window. `activateWindow()` later reveals it.

   ```tsx
   render(<App />, {
     title: "Notes",
     focus: process.env.GPUIX_BACKGROUND !== "1",
   });
   ```

   ```ts
   const app = await launch({
     command: "bun",
     args: ["app.tsx"],
     env: { GPUIX_BACKGROUND: "1" },
   });
   await app.getByTestId("composer").fill("hello gpuix");
   await app.getByTestId("composer").press("enter");
   ```

   Linux currently ignores `focus` and `show`.

3. **Pixel-stable bidirectional history with `<virtual-list>`.** `scrollToItem` accepts an offset inside the row. `getListScrollTop` returns `[itemIndex, offsetInItemPx, viewportHeightPx]`. Infinite histories can prepend or append a page without moving the message under the reader. `PublicInstance` is exported for typed host refs. See `examples/infinite-chat.tsx`.

   ```tsx
   renderer.scrollToItem(listId, index, offsetInItem);
   const top = renderer.getListScrollTop(listId);
   ```

4. **Custom renderers implement one atomic `applyBatch(json)` transport.** Separate mutation methods are gone from `NativeRenderer`. Style and custom-prop payloads are JSON values inside the batch.

   ```ts
   const renderer: NativeRenderer = {
     applyBatch(json) {
       return nativeTransport.applyBatch(json);
     },
   };
   ```

5. **The WebGPU chat example is live at** [https://gpuix.dev/chat-example/](https://gpuix.dev/chat-example/). The bidirectional history example is also served at `/infinite` from `bun run web`.

6. **One prebuilt binary per OS.**

   | OS      | Target                     | Renderer      |
   | ------- | -------------------------- | ------------- |
   | macOS   | `aarch64-apple-darwin`     | Metal         |
   | Linux   | `x86_64-unknown-linux-gnu` | Vulkan / wgpu |
   | Windows | `x86_64-pc-windows-msvc`   | Direct3D      |

   Intel macOS, arm64 Linux, and arm64 Windows have no prebuilt packages. macOS and Linux chat examples ship as `.tar.gz`.

   ```bash
   tar -xzf example-chat-aarch64-apple-darwin.tar.gz
   ./example-chat-aarch64-apple-darwin
   ```

7. **Text selection and native editing.** Soft-wrapped washes include the first glyph of the next visual row. Virtual-list selection survives unmounts, scrolls at the edge, and stops when the list cannot move. Double-click selects a word in `<input>` and `<textarea>`. Triple-click selects the full value. Adjacent typing groups into one undo step for 700 ms.

8. **CRLF source no longer leaves carriage returns in `<code>`.** Rendering, highlighting, selection, and copied text use normalized LF rows.

Fixes [https://github.com/remorses/gpuix/issues/25](https://github.com/remorses/gpuix/issues/25)
</Update>

<Update id={"@gpuix/react@0.5.1"} label={"Aug 26, 2026"}>

## @gpuix/react\@0.5.1

1. **Fixed `@gpuix/react/testing` reporting no native renderer when installed from npm.** `hasNativeTestRenderer` was always `false`, so every suite that guards on it skipped silently:

   ```
   Test Files  1 skipped (1)
        Tests  6 skipped (6)
   ```

   `testing.js` ships as ESM and loaded the addon with a bare `require("@gpuix/native")`. Node has no `require` in ESM. Inside this repository vitest inlines the workspace package and provides one, so the suite here always passed; installed from npm the package is externalized and run by Node, the call threw, and the `catch` reported native as missing. It now uses `createRequire(import.meta.url)`.

See [@gpuix/react@0.5.0](https://github.com/remorses/gpuix/releases/tag/%40gpuix%2Freact%400.5.0) for the feature release this patches, including the browser renderer, the `highlight` prop and the macOS menu bar.
</Update>

<Update id={"@gpuix/react@0.5.0"} label={"Aug 26, 2026"}>

## @gpuix/react\@0.5.0

1. **GPUIX apps now run in the browser.** The same React tree renders through GPUI's browser platform on WebGPU, with a WebGL2 fallback. `RetainedTree`, `GpuixView`, styles, and text painting are shared with desktop, so events, selects, comboboxes, inputs, motion, and GPUI scroll gestures all work through a Wasm-to-JavaScript callback bridge. napi-rs stays the desktop bridge; wasm-bindgen starts `gpui_web` in the page.

   ```sh
   bun run web       # build the Wasm if it is missing, then serve with HMR
   bun run web:wasm  # only cargo + wasm-bindgen
   ```

   `bun run web` serves through Bun's frontend dev server, so an edit to a component module is a **React Fast Refresh** update instead of a page reload. `useState` survives, the GPUI canvas is never re-created, and the \~19 MB Wasm module is never re-fetched.

   Browser apps always expose the automation API on `globalThis`, so Playwright or Playwriter can drive them by evaluating in the page:

   ```ts
   await globalThis.gpuix.getByTestId("send").click();
   await globalThis.gpuix.getByTestId("composer").fill("hello");
   await globalThis.gpuix.clock.fastForward(200);
   ```

   Two rules for a browser entry, both learned the hard way: never call `import.meta.hot.accept("./your-app", ...)` in the entry file, because Bun runs the dependency-accept callback even when the module already self-accepted for Fast Refresh and the remount wipes every hook; and keep the `@gpuix/native` import out of any Refresh boundary, because the Wasm half is a singleton and `WebGpuixRenderer::init` fails with `GPUIX web is already running`.

   Browser-specific fixes that landed with it: the debug frame overlay works on Wasm (`render(<App />, { debugFrameOverlay: 'full' })`), macOS browsers get Option+Left / Option+Right word navigation in inputs, diagonal resize cursors point the right way, and GPUI Web's IME bridge is fully hidden so host `input` CSS can no longer unhide a stray text field at the top of the page.

   On iOS, touch pans emit **scroll wheel** events instead of mouse drags, so a swipe scrolls instead of selecting text. A tap does not start a selection, a long press followed by a drag still does, and a text input requests the software keyboard inside its tap handler so the keyboard opens on the composer and closes elsewhere.

2. **New `highlight` prop** — paint a background wash behind matched or explicitly given text ranges. This is what you need for Ctrl+F, agent citations, or LSP diagnostic tints. Put it on any element and it applies to that subtree, so the root searches the window and a container searches only that container.

   ```tsx
   <div highlight={{ query: "fox" }}>
     <text>the quick brown fox</text>
   </div>
   ```

   It reaches `<text>`, `<code>`, `<markdown>` and `<diff>` with no extra props, because every string GPUIX paints goes through the same funnel.

   `useTextSearch` owns the cursor and the count, so a find bar needs no effects:

   ```tsx
   import { useTextSearch } from '@gpuix/react'

   const search = useTextSearch({ query })

   <text>{search.total === 0 ? 'No results' : `${search.active + 1}/${search.total}`}</text>
   <div onClick={search.previous}><text>↑</text></div>
   <div onClick={search.next}><text>↓</text></div>

   <div {...search.props} style={{ flex: 1 }}>
     <Transcript />
   </div>
   ```

   | field                   | meaning                                                   |
   | ----------------------- | --------------------------------------------------------- |
   | `query`                 | substring to match, case-insensitive by default           |
   | `caseSensitive`         | exact case only                                           |
   | `wholeWord`             | neither neighbour may be alphanumeric or `_`              |
   | `ranges`                | explicit `[start, end)` UTF-16 pairs                      |
   | `color` / `activeColor` | any CSS colour; defaults come from the theme              |
   | `activeIndex`           | which match gets `activeColor`, for a find cursor         |
   | `matchIndexOffset`      | matches before this subtree; only for virtualized content |
   | `radius`                | corner radius of the wash, default 2                      |

   Matches are non-overlapping and leftmost-first, and never cross a line, exactly like browser find. They do cross the several host nodes React creates for one interpolated line: `<text>Hello {name}!</text>` is three host text nodes and `Hello Tommy` still matches. `activeIndex` counts matches in paint order, so it means the same thing whether a match sits in a `<text>` or inside a `<code>` block.

   A `<virtual-list>` never builds off-screen rows, so the app supplies both numbers with the new `findRanges` export, which runs the same algorithm as the native matcher on a string you give it:

   ```tsx
   import { findRanges, useTextSearch } from "@gpuix/react";

   const perRow = useMemo(
     () => rows.map((row) => findRanges({ text: row.text, query }).length),
     [rows, query],
   );

   const search = useTextSearch({
     query,
     matches: {
       total: perRow.reduce((n, count) => n + count, 0),
       indexOffset: perRow
         .slice(0, windowStart)
         .reduce((n, count) => n + count, 0),
     },
   });
   ```

   A highlight is a quad, so `getPaintedText()` cannot see it. `renderer.getPaintedHighlights()` reports the matched range in UTF-16 units plus the boxes it drew, one per visual row.

   Nothing resolves and nothing paints unless an element declares a `highlight`. A root-scoped query over a 1000-turn chat costs about 2ms per keystroke, and moving the find cursor only re-colours matches it already found.

3. **`<virtual-list>` can mount a window of rows** instead of all of them. The children form retains every child, so the first mount of a long transcript used to pay for every row. Pass `itemCount` with `estimatedItemHeight` and `windowStart`, then render only that slice; native keeps the full logical length for the scrollbar.

   ```tsx
   const WINDOW = 40;

   function Transcript({ turns }: { turns: Turn[] }) {
     const [start, setStart] = useState(0);
     const end = Math.min(turns.length, start + WINDOW);
     return (
       <virtual-list
         itemCount={turns.length}
         windowStart={start}
         estimatedItemHeight={220}
         onVisibleRange={(event) =>
           setStart(Math.max(0, Math.floor(event.startIndex ?? 0) - WINDOW / 4))
         }
       >
         {turns.slice(start, end).map((turn) => (
           <ChatTurn key={turn.id} turn={turn} />
         ))}
       </virtual-list>
     );
   }
   ```

   `onVisibleRange` reports `startIndex` and `endIndex` after a scroll. TypeScript now **requires** `estimatedItemHeight` next to `itemCount`, and native ignores `itemCount` without it, because a row React has not mounted would otherwise measure as height 0 and collapse the scrollbar on a jump.

   There is deliberately **no `VirtualList` wrapper component**. The window is application state. A generic wrapper cannot know when to widen its own window, so it silently dropped rows whenever `itemCount` grew without a scroll, which is exactly what a filter does.

4. **A prepended row is visible again.** A list is anchored on a row, not a pixel offset, so inserting rows above the viewport used to slide the viewport down by the height of the new rows. A todo list or a feed that prepends the newest item never showed it.

   ```text
   scrolled down                          pinned to the top
   ┌──────────────────┐                   ┌──────────────────┐
   │ new row  (above) │  ◄── inserted     │ new row          │  ◄── inserted, visible
   ├──────────────────┤                   ├──────────────────┤
   │ ░░ viewport ░░░░ │  stays put        │ ░░ viewport ░░░░ │  follows the insert
   │ ░░░░░░░░░░░░░░░░ │                   │ ░░░░░░░░░░░░░░░░ │
   └──────────────────┘                   └──────────────────┘
   ```

   A browser anchors the same way and suppresses it at `scrollTop: 0`. A top-aligned list that is scrolled to the very top now stays at the top across a mutation. Scrolled anywhere else, the rows under the pointer still do not move. A history pane that loads older pages while the user reads should keep using `alignment="bottom"`.

5. **Automation can drag, hover, wheel, and hold modifiers.** The protocol already carried the events, but nothing exposed them, so a drag or a pan could not be driven from a test.

   ```ts
   await app.getByTestId("clip-7").dragBy(120, 0, { steps: 6 });
   await app.getByTestId("clip-7-trim-end").dragTo(app.getByTestId("clip-8"));
   await app.getByTestId("canvas").wheel(0, 120, { modifiers: "cmd" });
   await app.getByTestId("row-3").hover();

   await app.mouse.drag({ x: 240, y: 500 }, { x: 700, y: 620 });
   await app.mouse.wheel({ x: 700, y: 600 }, -140, 0);
   await app.mouse.down({ x: 100, y: 100 }, { button: 2 });
   ```

   | Call                                                | What it does                                                       |
   | --------------------------------------------------- | ------------------------------------------------------------------ |
   | `locator.hover()`                                   | Moves the pointer to the center, so hover styles and tooltips fire |
   | `locator.wheel(dx, dy)`                             | One wheel event over the center                                    |
   | `locator.dragBy(dx, dy)` / `locator.dragTo(target)` | Press, travel, release                                             |
   | `locator.center()`                                  | The center of the last painted bounds                              |
   | `app.mouse.move / down / up / click / wheel / drag` | Raw pointer input in window coordinates                            |

   A drag sends **interpolated moves**, not one jump, because snapping, live previews, and per-move commits only appear when the pointer travels. Every mouse call takes `modifiers` in the same hyphenated syntax as `press('cmd-a')`, so cmd-wheel zoom, shift-click range selection, and alt-drag duplication are testable. `launch()` can now scroll a live app, `textContent()` concatenates descendants like DOM `textContent`, and `click({ button })` really sends that button. Mouse input, locator bounds, and clock controls also work against a live app on Windows, Linux, and FreeBSD.

6. **`<input>` and `<textarea>` are reachable from the locator API.**

   ```ts
   await app.getByTestId("composer").click();
   await app.getByTestId("composer").fill("hello gpuix");
   ```

   `bounds()` and `click()` threw `Element has no painted bounds`, because a custom element paints itself and the editor never attached the automation bounds tracker; the only workaround was a hard-coded pixel coordinate. In the browser, `fill()` and `press()` threw `GPUI browser input is unavailable`: the client looked for `input[data-gpui-input]`, and [zed-industries/zed#63201](https://github.com/zed-industries/zed/pull/63201) replaced that element with a `<textarea>`. It now matches the attribute alone, exported as `IME_MIRROR_SELECTOR`.

   `<img>`, `<svg>`, `<anchored>`, `<diff>` and `<markdown>` do register painted bounds now too, so a `testId` on `<markdown>` no longer returns null, and `TestRenderer.findByTestId()` resolves it from the retained tree.

7. **macOS apps have a menu bar**, so `⌘Q`, `⌘H`, `⌥⌘H`, `⌘M` and `⌘W` work. GPUI never calls `NSApplication.setMainMenu:`, so `NSApp.mainMenu` stayed nil, macOS painted nothing next to the Apple menu, and there was no way to quit a GPUIX app from the keyboard.

   ```
   Apple    <executable>             Window
            ├ Services               ├ (AppKit window tiling)
            ├ Hide <appName>   ⌘H    ├ Minimize          ⌘M
            ├ Hide Others     ⌥⌘H    ├ Zoom
            ├ Show All               ├ Close Window      ⌘W
            └ Quit <appName>   ⌘Q    └ (open windows)
   ```

   New `appName` window option for the name inside `Hide X` and `Quit X`. It defaults to `title`.

   ```tsx
   render(<App />, { title: "Todo", appName: "Todo" });
   ```

   `appName` does **not** set the title of the application menu: macOS takes that from the executable, so `bun app.tsx` shows `bun`. Only a real `.app` bundle changes it. There is no Edit menu on purpose, because AppKit consumes a menu key equivalent before the window sees it and `⌘C` would be taken away from text selection and from `<input>`.

8. **Pointer capture, like HTML.** `onMouseMove` and `onMouseUp` continue after the pointer leaves the element that received `onMouseDown`, matching [`setPointerCapture`](https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture). A clip, resizer, or slider keeps receiving events without a full-window overlay.

   ```tsx
   <div
     onMouseDown={(e) => startDrag(e)}
     onMouseMove={(e) => moveDrag(e)}
     onMouseUp={() => endDrag()}
   />
   ```

   Capture is armed only when the same node listens for down and move. A node with only `onMouseDown` / `onMouseUp` does not capture, and a release outside still cancels the click, as in the DOM.

9. **The wheel reaches an ancestor scroller from under an absolutely positioned child**, like a browser. Absolute and fixed boxes used **BlockMouse**, which ended the hit test, so a timeline clip or a graph node swallowed a pan gesture. Every filled or positioned `div` now uses **BlockMouseExceptScroll**: clicks and hovers stop, the wheel passes through.

   ```tsx
   <div style={{ position: "relative" }} onScroll={pan}>
     {/* the wheel over this clip now pans the surface behind it */}
     <div
       style={{
         position: "absolute",
         left: 240,
         width: 120,
         backgroundColor: "#38455C",
       }}
     />
   </div>
   ```

   Set `pointerEvents: "auto"` on the rare element that must swallow the wheel too, such as a modal backdrop. `<anchored>` still occludes by default. An absolutely positioned box still takes clicks with no background, exactly like an empty positioned `div` in a browser, so a wrapper that only carries a scroll offset should set `pointerEvents: "none"`.

10. **`<code>` is a bare surface.** It paints glyphs only: no fill, no border, no radius, no padding, no language header. `style` is the surface, exactly like a `<div>`, so the card look belongs to your app instead of to the element.

    ```tsx
    <code
      code={source}
      language="typescript"
      showLineNumbers
      style={{
        padding: 12,
        borderRadius: 10,
        borderWidth: 1,
        borderColor: "#ffffff1f",
        backgroundColor: "#ffffff09",
      }}
    />
    ```

    `fontFamily`, `fontSize`, `fontWeight`, `lineHeight` and `color` in `style` now beat the theme, and one resolver feeds the div text style, every `TextRun`, and the fixed row height. `style.lineHeight` used to be dropped and clip tall glyphs; it re-sizes the rows instead.

    **Migration:** `showHeader` is gone. Render your own header in a wrapper. Five `theme.metrics` fields only ever styled that card and moved to the `mdCode*` group, where they still tune the `<markdown>` fenced block:

    | Before                          | After                               |
    | ------------------------------- | ----------------------------------- |
    | `codePaddingX` / `codePaddingY` | `mdCodePaddingX` / `mdCodePaddingY` |
    | `codeRadius`                    | `mdCodeRadius`                      |
    | `codeHeaderPaddingY`            | `mdCodeHeaderPaddingY`              |
    | `codeHeaderTextSize`            | `mdCodeHeaderTextSize`              |

    `<markdown>` keeps its card: a document renderer owns its layout, a primitive does not.

11. **Syntax highlighting moved from Tree-sitter to Syntect**, with **Oniguruma** on native. There is no Tree-sitter runtime and no per-language C grammar in the binary. Language detection is unchanged (fence tag, then path, then shebang), and token classes stay `HighlightKind` values rather than baked-in colours, so a theme change recolours existing spans without a reparse.

    Syntect compiles every TextMate regex of a grammar the first time that grammar is used, on the frame thread, inside a paint. The engine decides how expensive that is:

    | grammar    | fancy-regex, first use | **Oniguruma, first use** |
    | ---------- | ---------------------: | -----------------------: |
    | TypeScript |                \~133ms |               **\~12ms** |
    | Markdown   |                 \~39ms |              **\~1.7ms** |
    | Rust       |                 \~17ms |              **\~1.6ms** |

    The chat example mount for 1000 turns goes from about **240ms to about 130ms**, and the worst scroll frame from about **17ms to about 6ms**. The browser Wasm build keeps the pure-Rust fancy-regex engine, because Oniguruma is a C library. Token colours can shift a little versus Tree-sitter, because Syntect scopes are not the old capture names.

12. **A large mount is 4x faster and the retained tree is 5x smaller.** `applyBatch` used to build a `serde_json::Value` tree, deep-clone every style payload out of it, and parse the clone a second time, so each style was allocated three times. The batch now deserializes straight from its JSON bytes into typed ops, and styles are shared by content: a 10,000-turn chat sends 59,320 `setStyle` ops carrying 90 distinct styles, and every element gets the same `Arc`.

    Measured on a 10,000-turn chat, 221,764 ops:

    |                   |    before |    after |
    | ----------------- | --------: | -------: |
    | parse and apply   |  127.1 ms |  30.1 ms |
    | heap churn        |  900.5 MB | 104.0 MB |
    | allocations       | 1,476,196 |  186,090 |
    | retained tree     |  224.5 MB |  42.6 MB |
    | bytes per element |    3116 B |    592 B |

    A 5,000-row chat also stops rebuilding virtual-list focus maps on every GPUI frame, so sidebar motion and caret blink no longer pay that cost per tick, and custom-element props are only re-parsed when a retained value actually changes. `getAutomationTree()` stops serializing style, events, and custom props, which took a 5k-row tree from about 110ms to about 22ms, so `getByTestId().click()` is no longer dominated by encoding unused style maps.

13. **The install is about 8x smaller.** `@gpuix/native` packed every platform binary into the main tarball through a `*.node` glob, on top of the six per-platform packages that `optionalDependencies` already resolves. A hello-world install paid for all of it:

    ```
    node_modules                       254M
    ├── @gpuix/native                  185M  ◄── all six binaries, unused
    ├── @gpuix/native-darwin-arm64      23M  ◄── the one that loads
    └── @gpuix/react                   544K
    ```

    Only the loader, the types, the browser entry, and the Wasm build ship in the main package now. Nothing changes at runtime.

14. **Fixed Windows x64 native binding failing to load with `ERR_DLOPEN_FAILED`.** The published `.node` statically imported `TaskDialogIndirect` from comctl32 v6 and `u_strlen` from `icuuc.dll`. Node and Bun do not activate comctl32 v6, so Windows resolved the old comctl32 and `LoadLibrary` failed before any JS ran.

    ```bash
    bun -e "require('@gpuix/native'); console.log('OK')"
    ```

15. **Every CSS `cursor` keyword GPUI can paint is supported**, not just `pointer` and `default`. Resize and drag cursors are what tell a user that an edge can be trimmed or a clip can be grabbed; until now `col-resize` was silently dropped.

    ```tsx
    <div style={{ cursor: 'grab', active: { cursor: 'grabbing' } }} />
    <div style={{ cursor: 'col-resize' }} />
    ```

    | Group    | Keywords                                                                                                                                                                               |
    | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | Pointing | `default`, `auto`, `pointer`, `context-menu`, `not-allowed`, `no-drop`                                                                                                                 |
    | Text     | `text`, `vertical-text`, `crosshair`                                                                                                                                                   |
    | Dragging | `grab`, `grabbing`, `move`, `all-scroll`, `alias`, `copy`                                                                                                                              |
    | Resizing | `col-resize`, `row-resize`, `ew-resize`, `ns-resize`, `nwse-resize`, `nesw-resize`, `n-resize`, `e-resize`, `s-resize`, `w-resize`, `ne-resize`, `nw-resize`, `se-resize`, `sw-resize` |

    `cursor` is a typed union, so an editor completes the list. An unlisted keyword is ignored, like any other invalid style value.

16. **Colour strings accept the full csscolorparser grammar** across styles, themes, pseudo-states, selection colours, SVG tint, borders, and shadows: modern RGB/HSL/HWB, HSV, LAB/LCH, OKLab/OKLCH, named colours, `transparent`, alpha, `none`, and limited relative-colour forms. TypeScript types are unchanged.

17. **More style properties reach the GPU.** Per-side border widths and one structured `boxShadow` with offset, blur, spread, and colour are new. Per-corner radii, `flexBasis`, and `alignContent` were already declared in the public style type but never applied; they work now.

18. **New `onAuxClick` for the non-primary mouse buttons.** `onClick` never fired for a right or middle click, so the `isRightClick` field it documents could never be `true` and a context menu had no event to hang on. `onClick` stays primary-only, like the DOM.

    ```tsx
    <div
      onClick={() => select(item)}
      onAuxClick={(event) => {
        if (event.isRightClick) openContextMenu(event.x, event.y);
      }}
    />
    ```

    `onMouseDown` and `onMouseUp` still see every button through `event.button`: `0` left, `1` middle, `2` right.

19. **Window geometry hooks are pull-based.** `useWindowSize()` seeded state with a hardcoded `800x600` and read the renderer once from an effect, so a first read before the platform window had a size kept `800x600` forever, and a resize was never observed at all. It samples every **100 ms** now and only rerenders when the numbers change.

    New `getWindowInsets()` and `useWindowInsets()` report system and software-keyboard geometry, so a composer can stay above the iOS keyboard instead of hiding behind it:

    ```tsx
    const { keyboardTop, keyboardVisible, ime } = useWindowInsets();

    return (
      <div style={{ paddingBottom: ime.bottom }}>
        {keyboardVisible
          ? `Keyboard starts at ${keyboardTop}px`
          : "Keyboard closed"}
      </div>
    );
    ```

    | Field             | Meaning                                                  |
    | ----------------- | -------------------------------------------------------- |
    | `ime`             | Edges covered by the software keyboard                   |
    | `safeArea`        | Edges covered by notches, status bars, home indicators   |
    | `effective`       | Per-edge max of the two, the region content should avoid |
    | `keyboardTop`     | Y coordinate where the keyboard starts                   |
    | `keyboardVisible` | `ime.bottom > 0`                                         |
    | `visibleHeight`   | Window height minus the effective top and bottom         |

    Both hooks take the same option, because Safari fires `visualViewport` events in bursts while the keyboard animates and iOS reports stale values on some of them:

    ```tsx
    useWindowInsets(); // 100ms, the default
    useWindowInsets({ intervalMs: 250 }); // slower
    useWindowInsets({ intervalMs: false }); // read once, never poll
    ```

20. **One diagonal gesture scrolls both axes**, and `position: "fixed"` lays out. `overflow: "scroll"` moved only one axis per wheel event, because GPUI zeroes the smaller of the two deltas by default.

    ```tsx
    <div style={{ width: 260, height: 220, overflow: "scroll" }}>
      {/* one diagonal swipe now pans on X and Y together */}
    </div>
    ```

    A flex column stretches its children to the cross axis, so rows in a two-axis container still need to state a width, or there is nothing to pan on X. `position: "fixed"` blocked hits like `absolute` but stayed in normal flow, so a box drifted when its siblings changed; it now lays out like `absolute`.

21. **Text selection starts from the empty space before the glyphs.** A press in parent padding, a code gutter, or the empty start of a line clamps to the nearest text on that row, instead of requiring the mouse-down to land inside the tight text box.

    ```
      [padding] hello world
          ^
          press here, drag right  →  "hello world"
    ```

    A press above or below every line still does not start a selection, so a composer or titlebar cannot claim the nearest paragraph, and `userSelect: "none"` now also blocks the start.

    Copying across interpolated text is fixed too. `<text>Hello {name}!</text>` is three painted runs of one line, and selecting across them used to copy them joined with newlines. Runs now carry the parent host element they belong to, so the same selection yields `Hello Tommy!`, while `<code>`, `<diff>` and `<markdown>` keep one line per line.

22. **Fixed `key` on every GPUIX element.** A list built with `.map()` failed to typecheck, so any real app broke on the first `tsc` run:

    ```
    error TS2322: Type '{ key: string; ... }' is not assignable to type 'Props'.
      Property 'key' does not exist on type 'Props'.
    ```

    `key` lives on `Props` now, next to `ref`. It cannot live on `JSX.IntrinsicAttributes`, because TypeScript 5 ignores that member for intrinsic elements. Every element prop type extends `Props`, so `<div>`, `<text>`, `<img>`, `<svg>`, `<canvas>`, `<input>`, `<textarea>`, `<anchored>`, `<code>`, `<diff>`, `<markdown>` and `<virtual-list>` accept `key` again, and so do `motion.div`, Select, Combobox and Tooltip. `@gpuix/react/jsx-dev-runtime` types also match the runtime file now: they re-exported `jsx` and `jsxs` from `react/jsx-dev-runtime`, which exports only `jsxDEV`.

23. **Abandoned concurrent renders stay out of the native mutation queue.** React may throw away a Suspense render. GPUIX waits until commit before it creates native elements, so fallback text paints and abandoned text does not. Unchanged click handlers also stay registered across rerenders, because the whole handler map is no longer cleared before every update.

24. **Each React root owns its event handler map.** Two `createTestRoot()` trees can both start at id `1` without overwriting each other's handlers, and a remount on the same native renderer keeps allocating new ids, so a late event from the old tree cannot hit a new handler that reused id `1`.

    **Migration:** `resetIdCounter()` is gone, and `handleGpuixEvent` needs the renderer that produced the event:

    ```ts
    handleGpuixEvent(event, renderer);
    ```

25. **Native `<markdown>` wraps in flex columns.** A markdown node in a flex row kept its max-content width, so a long paragraph or list item blew past the parent. The root and each text block shrink with `min-width: 0` now, and a fenced block inside `<markdown>` matches `<code>`: long lines scroll on X and leave the vertical wheel on the parent.

    ```tsx
    <div style={{ display: "flex", flexDirection: "row", width: 280 }}>
      <div style={{ width: 40, flexShrink: 0 }} />
      <markdown
        source="- a long sentence that must wrap in the remaining column"
        style={{ flexGrow: 1 }}
      />
    </div>
    ```

26. **The test renderer runs on Windows** through GPUI's DirectX renderer: `TestGpuixRenderer`, `createTestRoot()`, native input simulation, and PNG screenshot capture. A live window can call `captureScreenshot()` there too. Linux stays unavailable until GPUI ships its pending wgpu headless renderer.

    The test app also releases its custom elements before the GPUI app goes away. `<input>` keeps a GPUI entity handle, and GPUI's leak detector panics if one outlives the app, which killed the whole vitest worker on Windows after every test in the file had already passed. `createTestRoot({ width, height })` does not size the window on Windows yet: it opens at the display size. Tracked in [#21](https://github.com/remorses/gpuix/issues/21).

    `createTestRoot()` can also size the offscreen window, which was always **1280x800**. That is wide enough to keep a centered `maxWidth` column at its cap, so any layout that only changes below a breakpoint was invisible to the suite.

    ```tsx
    const narrow = createTestRoot({ width: 640, height: 480 });
    createTestRoot({ width: 640 }); // 640 x 800
    createTestRoot({ width: 0 }); // throws: must be a positive, finite number
    ```

27. **New `getDebugFrameOverlayStats()`** so tests and apps can read the same draw times the on-screen overlay shows.

    ```ts
    renderer.resetDebugFrameOverlayStats();
    // ... scroll or click ...
    const stats = renderer.getDebugFrameOverlayStats();
    // stats.currentMs, stats.p90Ms, stats.p99Ms, stats.maxMs, stats.frames, stats.samples
    ```

    `p90Ms` is the overlay **10%** line and `p99Ms` is the **1%** line: the slow tail, not the fast frames.

    On macOS, `THROTTLE=utility` restarts a run under `taskpolicy -c utility`, which pins work to E-cores as an M1/M2 Air CPU proxy. `background` and `maintenance` are slower. GPU and RAM stay on the host machine, so this is not Chrome 6x, and it should not be set in CI.

    ```bash
    THROTTLE=utility bun run test chat.perf.test.tsx
    THROTTLE=utility bun --hot chat.tsx
    ```

28. **A Quickstart and a todo starter app.** The README described the architecture and the mutation protocol before it ever said how to install the packages, and never mentioned `jsxImportSource`, which is required: without it TypeScript falls back to DOM types and `<virtual-list>`, `<markdown>`, `<code>` and `style.hover` all fail.

    ```bash
    bun add @gpuix/react react
    bun add -d @types/react typescript
    ```

    ```json
    {
      "compilerOptions": {
        "jsx": "react-jsx",
        "jsxImportSource": "@gpuix/react"
      }
    }
    ```

    `example-app/` is a complete todo app in one file, with scripts already wired:

    | Script               | What it does                                 |
    | -------------------- | -------------------------------------------- |
    | `bun run dev`        | Desktop app with hot remount                 |
    | `bun run build`      | Standalone binary in `dist/todo`             |
    | `bun run web:dev`    | Browser build served with isolation headers  |
    | `bun run screenshot` | Drives the app through the automation client |
    | `bun run test`       | Vitest against the GPU test renderer         |
    | `bun run typecheck`  | `tsc --noEmit`                               |

    It shows `<virtual-list>`, a native `<input>`, `motion.div`, tinted `<svg>` icons, native `hover` and `active`, and `testId` automation hooks. Copy the folder, change `@gpuix/react` from `workspace:^` to a version range, and run `bun install`.

29. **A video-editor timeline example**, to answer whether GPUIX can carry a real editing surface. It drags clips between tracks, trims both edges with snapping, scrubs a playhead, marquee-selects, zooms under the pointer, and pans on both axes with a frozen ruler and a frozen track column.

    ```bash
    cd examples && bun --hot timeline.tsx
    ```

    Two patterns in it are worth copying. **React owns the scroll offset**: a native `overflow: "scroll"` grid cannot drive a frozen header, because GPUI moves the grid on the wheel frame and the `onScroll` callback arrives a frame later, so the two tear apart during a fast pan. **A drag needs no overlay**: each clip and trim handle listens for `onMouseDown`, `onMouseMove` and `onMouseUp`, which arms pointer capture, so a release past the window edge still ends the gesture, while an overlay mounted on the press cannot arm anything.

    A pannable surface also has to cull. On 3,259 clips across 26 tracks, one wheel frame costs **7.7ms** culled and **92ms** with `memo` alone.

30. **GitHub releases include a standalone chat example executable for each platform.** No Node, Bun, or Rust install is required.

    ```bash
    chmod +x example-chat-aarch64-apple-darwin
    ./example-chat-aarch64-apple-darwin
    ```

    macOS may block the unsigned binary the first time: right-click the file, choose Open, and confirm. On Windows, download `example-chat-x86_64-pc-windows-msvc.exe` and double-click it.

31. **`@gpuix/native` and `@gpuix/react` are published as Apache-2.0.** Both packages declare `license: Apache-2.0` and ship the license text in the npm tarball. GPUI itself is Apache-2.0, so this matches the native dependency.

32. Smaller fixes: `destroyElement` no longer leaves a dangling child id on the parent or skips invalidating the parent chain, so a cache keyed on the subtree revision cannot serve text that left the tree; automation calls after `close()` are rejected and shutdown is idempotent across the in-process and SSE backends.

---

Closes [#1](https://github.com/remorses/gpuix/issues/1), [#2](https://github.com/remorses/gpuix/issues/2) (Windows native binding failed to load) and [#20](https://github.com/remorses/gpuix/issues/20) (mouse move and up were dropped after a mouse-down rerender).

Known gap: `createTestRoot({ width, height })` does not size the window on Windows yet, tracked in [#21](https://github.com/remorses/gpuix/issues/21).
</Update>

<Update id={"@gpuix/react@0.4.0"} label={"Aug 23, 2026"}>

## @gpuix/react\@0.4.0

Also ships **@gpuix/native\@0.4.0**. CI publishes both packages.

1. **Native `motion.div` animations** — animate from an initial style to a target style. React sends the targets once. Rust interpolates the presentation style and requests GPUI frames. The React tree is not reconciled on each frame.

   ```tsx
   import { motion } from "@gpuix/react";

   <motion.div
     initial={{ width: 0, opacity: 0 }}
     animate={{ width: 260, opacity: 1 }}
     transition={{ duration: 0.2, ease: "easeOut" }}
   >
     Sidebar content
   </motion.div>;
   ```

   Numeric targets: `width`, `height`, `top`, `right`, `bottom`, `left`, `opacity`, `borderRadius`. Timing uses seconds. `ease` is `"linear"`, `"ease"`, `"easeIn"`, `"easeOut"`, `"easeInOut"`, or a cubic-bezier `[x1, y1, x2, y2]`.

   Set `initial={false}` to mount at the first `animate` target. A running animation can reverse or change target without a jump.

2. **Playwright-like automation API** — mark elements with `testId`, then drive them from tests or from another process.

   ```ts
   import { connectTest } from "@gpuix/react/automation";

   const app = await connectTest(renderer);
   await app.getByTestId("inc").click();
   await app.getByText("Count: 1").waitFor();
   await app.getByTestId("composer").fill("hello gpuix");
   await app.getByTestId("composer").press("enter");
   await app.captureFrames("review/sidebar", [0, 150, 300]);
   ```

   Locators: `getByTestId`, `getByText`, `getByType`. `app.clock.pause()`, `set(ms)`, and `fastForward(ms)` freeze native motion time.

   A live app listens on stdin when stdin is a pipe. `launch({ command, args })` pipes stdin and speaks SSE `data:` lines:

   ```ts
   import { launch } from "@gpuix/react/automation";

   const app = await launch({ command: "bun", args: ["examples/chat.tsx"] });
   await app.getByTestId("composer").fill("hello");
   await app.screenshot({ path: "live.png" });
   await app.close();
   ```

</Update>

<Update id={"@gpuix/react@0.3.0"} label={"Aug 23, 2026"}>

## @gpuix/react\@0.3.0

Also ships **@gpuix/native\@0.3.0**. CI publishes both packages.

1. **CSS grid on `div`** — `display: "grid"` plus `gridTemplateColumns` maps to GPUI's Taffy grid. Use `gridColumnMin: "max-content"` for tables so each column is as wide as its widest cell.

   ```tsx
   <div
     style={{
       display: "grid",
       gridTemplateColumns: 3,
       gridColumnMin: "max-content",
       rowGap: 1,
       columnGap: 1,
     }}
   >
     {cells}
   </div>
   ```

   `gridTemplateRows` and `gridRowMin` work the same on the other axis.

2. **Window chrome at open time** — `render()` now honors a transparent titlebar, traffic-light position, and a blurred or transparent window background.

   ```tsx
   import { render } from "@gpuix/react";

   render(<App />, {
     title: "Waku",
     width: 1180,
     height: 820,
     titlebarTransparent: true,
     windowBackground: "blurred",
     trafficLightX: 16,
     trafficLightY: 17,
   });
   ```

   `windowBackground` is `"opaque"` (default), `"transparent"`, or `"blurred"`.

3. **`<diff>` flows with its parent** — it no longer owns a scroller unless you pass `scroll`. Use `maxLines` to keep a long patch short. Show more fires `onShowMore`.

   ```tsx
   const [open, setOpen] = useState(false)

   <diff
     patch={unifiedPatch}
     wordDiff
     maxLines={open ? undefined : 24}
     onShowMore={() => setOpen(true)}
   />
   ```

4. **Debug frame overlay** — see draw time on a live window.

   ```tsx
   render(<App />, { title: "My App", debugFrameOverlay: "full" });
   ```

   Modes are `hidden`, `minimal`, and `full`. The readout is draw time, not FPS. `8.3 MS` is about 120 Hz.

5. **Quit when the last window closes** — the red traffic-light button now exits the process.

6. **Overlays block hits, and `pointerEvents` works** — set `pointerEvents: "none"` to opt out. Set `pointerEvents: "auto"` to block even with no fill.

7. **Opaque Select, Combobox, and Tooltip surfaces** — `FloatingLayer` defaults to `backgroundColor: "#1A1A1A"`.

8. **`<svg>` icons paint on the first frame** — file paths and `data:image/svg+xml` URLs both work.

9. **`bun --hot` remounts no longer paint a black window**.

10. **Cmd+Delete and Cmd+Backspace** in `<input>` and `<textarea>` match the macOS system text field.

11. **Vertical wheel over `overflowX: "scroll"` stays on the parent**. Trackpad X still pans the wide child.

12. **Parent scroller takes the wheel over a filled in-flow `div`**.

13. **macOS scroll stays at the display rate** on expensive frames.

14. **Faster first React mount** — `applyBatch` sends styles and custom props as JSON values instead of double-encoded strings.

15. **Raw custom-prop values stay intact** — `<anchored side="top">` commits again.
</Update>

<Update id={"@gpuix/react@0.2.0"} label={"Aug 23, 2026"}>

## @gpuix/react\@0.2.0

Also ships **@gpuix/native\@0.2.0**. CI publishes both packages.

1. **Selectable text everywhere, plus `<code>`, `<diff>` and `<markdown>`** — every string GPUIX paints can be selected with a drag and copied with Cmd+C. A drag can start in a plain `<text>` and end inside a code block.

   ```tsx
   <div style={{ display: "flex", flexDirection: "column" }}>
     <text>drag from here</text>
     <code code={"and into this code block"} language="ts" />
   </div>
   ```

   Opt out with `userSelect: 'none'`. Read the selection with `renderer.getSelectedText()`.

   ```tsx
   <code code={source} language="typescript" showLineNumbers />
   <diff patch={unifiedPatch} wordDiff collapsedPaths={['pnpm-lock.yaml']} />
   <markdown source={readme} onLinkClick={(e) => open(e.value)} />
   ```

   Bundled languages: Rust, TypeScript, TSX, JavaScript, JSX, Python, Go, JSON, Bash, TOML, YAML, Markdown, HTML, CSS, C.

2. **Native `<input>` and `<textarea>`** — caret, mouse selection, IME, clipboard, undo/redo, and grapheme-safe deletion. `Enter` submits. `Shift+Enter` inserts a newline in a textarea.

   ```tsx
   <textarea
     value={draft}
     minRows={1}
     maxRows={8}
     onChange={(e) => setDraft(e.value ?? "")}
     onSubmit={send}
   />
   ```

3. **`render()` remounts React on the same native window** — `bun --hot` saves remount the tree without a second window.

   ```tsx
   import { render } from "@gpuix/react";
   render(<App />, { title: "My App", width: 800, height: 600 });
   ```

4. **Headless Select, Combobox, and Tooltip** — unstyled primitives. Import `@gpuix/react/select`, `@gpuix/react/combobox`, or `@gpuix/react/tooltip` and wrap them in local `components/ui` files.

   ```tsx
   import * as SelectPrimitive from "@gpuix/react/select";

   <SelectPrimitive.Root value={model} onValueChange={setModel}>
     <SelectPrimitive.Trigger>
       <SelectPrimitive.Value placeholder="Select a model" />
     </SelectPrimitive.Trigger>
     <SelectPrimitive.Content>
       <SelectPrimitive.Item value="sonnet">Sonnet</SelectPrimitive.Item>
     </SelectPrimitive.Content>
   </SelectPrimitive.Root>;
   ```

5. **`<virtual-list>`** — GPUI builds only rows near the viewport.

   ```tsx
   <virtual-list alignment="bottom" followTail estimatedItemHeight={180}>
     {messages.map((message) => (
       <Message key={message.id} message={message} />
     ))}
   </virtual-list>
   ```

6. **Tintable local SVG icons**

   ```tsx
   <svg
     src="/absolute/path/to/search.svg"
     style={{ width: 16, height: 16, color: "#b4b4b4" }}
   />
   ```

7. **`startFrameLoop()`** — idle CPU drops from \~73% to \~1%. Default pace is \~125fps.

   ```tsx
   import { startFrameLoop } from "@gpuix/react";
   startFrameLoop(renderer);
   ```

8. **Native GPUI platform** on macOS, Windows, and Linux. Windows runtime validation is still pending.

9. **GPUI upgrade to zed `d5dc01f2`**. Scroll events can report `touchPhase: 'cancelled'`. Building from source now needs Rust 1.97.1 and the Metal toolchain on macOS.

10. **Style props that were declared and dropped now work** — full styles on `<text>`, plus `fontSize`, `textAlign`, `rowGap`, `columnGap`, `lineHeight`, and `borderWidth: 0`.

11. **`autoFocus` works** and `<input>` no longer ships a hardcoded look.

12. **Blinking caret** every 500ms while focused. Colour is `theme.caret`.

13. **Clipboard and natural scroll** — Cmd+C writes to the system clipboard. Wheel deltas keep the OS sign.

14. **React 19 JSX components** can return any `ReactNode`.
</Update>
