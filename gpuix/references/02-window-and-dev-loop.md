# GPUIX — Windows, menus, background launch, frame overlay, hot reload

Verbatim sections usage–hot reload from [gpuix.dev](https://gpuix.dev/index.md) (`index.md` lines 665–1057). Images and anchor links are relative to that page.

## In this file

- [Usage](#usage)
- [Debug frame overlay](#debug-frame-overlay)
- [Hot reload](#hot-reload)

---

## Usage

```tsx
import React, { useState } from "react";
import { render } from "@gpuix/react";

function App() {
  const [count, setCount] = useState(0);
  return (
    <div style={{ display: "flex", gap: 8, padding: 16 }}>
      <div
        style={{
          backgroundColor: "#3b82f6",
          borderRadius: 8,
          padding: 12,
          cursor: "pointer",
        }}
        onClick={() => setCount((c) => c + 1)}
      >
        <div style={{ color: "#ffffff" }}>Count: {count}</div>
      </div>
    </div>
  );
}

render(<App />, {
  title: "My App",
  width: 800,
  height: 600,
  titlebarTransparent: true,
  windowBackground: "blurred",
  trafficLightX: 16,
  trafficLightY: 17,
});
```

`render()` creates the native window, mounts React, and starts the frame loop.
The red traffic-light button quits the process. Start the app again from the
terminal.

| Option                            | Values                                             | Purpose                                                                   |
| --------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------- |
| `titlebarTransparent`             | boolean                                            | Hide the native titlebar so the app draws chrome under the traffic lights |
| `windowBackground`                | `"opaque"` (default), `"transparent"`, `"blurred"` | Window fill. `"blurred"` is the macOS vibrancy backdrop                   |
| `trafficLightX` / `trafficLightY` | pixels                                             | Traffic-light origin. The chat example uses `(16, 17)`                    |
| `transparent`                     | boolean                                            | Same as `windowBackground: "transparent"` when that option is unset       |
| `appName`                         | string                                             | Name inside the macOS `Hide X` and `Quit X` items. Defaults to `title`    |
| `focus`                           | boolean, default `true`                            | `false` opens the window behind the active app, like `open -g`            |
| `show`                            | boolean, default `true`                            | `false` opens the window hidden. Call `activateWindow()` to reveal it     |

Call it again after a save and it remounts the tree on the same window.

### The macOS menu bar

GPUIX installs the application menu bar for you, so a fresh app already answers
`⌘Q`, `⌘H`, `⌥⌘H`, `⌘M`, and `⌘W`. Without it `NSApp.mainMenu` is nil, macOS
paints an empty menu bar, and those shortcuts do not exist at all: AppKit only
provides them through menu items.

```
Apple    <executable>             Window
         ├ Services               ├ (AppKit window tiling)
         ├ Hide <appName>   ⌘H    ├ Minimize          ⌘M
         ├ Hide Others     ⌥⌘H    ├ Zoom
         ├ Show All               ├ Close Window      ⌘W
         └ Quit <appName>   ⌘Q    └ (open windows)
```

**`appName` does not set the title of the application menu.** macOS takes that
from the executable, so `bun app.tsx` shows `bun` during development and a
`bun build --compile` binary shows its own file name. Only a real `.app` bundle
changes it. `appName` reaches the items inside the menu, and nothing else.

There is **no Edit menu**, on purpose. A menu key equivalent is consumed by
AppKit before the window sees the key event, so an Edit menu carrying `⌘C`
would take the keystroke away from text selection and from `<input>`.

Use **`render()`**, not `createRenderer()`, in the app entry. `bun --hot`
re-runs the whole file on save. `createRenderer()` plus `init()` would then
build a second host. `render()` is idempotent: the first call owns the window,
later calls only remount React.

`createRenderer()`, `createRoot()`, and `startFrameLoop()` stay public for
tests and custom hosts. Pass `{ renderer }` into `render()` when you already
have one.

**One renderer drives one root.** A renderer owns one window, one native root
id, and one event map, so `createRoot()` throws if that renderer already has a
mounted root. Call `unmount()` on the first root before you create another;
`render()` already does that for you.

### Background launch

`focus: false` opens the window **without taking focus**. The app you were
typing in keeps the caret and the active titlebar. `show: false` goes further
and opens no window at all, so the process runs with a live React tree and
nothing on screen.

```tsx
render(<App />, { title: "Notes", focus: false });
```

**Turn this on whenever a coding agent runs your app.** An agent that starts
the app to check its work will otherwise yank the window in front of whatever
you are doing, mid-sentence, once per iteration. With `focus: false` the agent
still gets a real GPU-rendered window it can screenshot and click, and you keep
your editor. See [Let an agent drive the app](#let-an-agent-drive-the-app).

`activateWindow()` brings the window forward and focuses it. It is the only way
to reveal a `show: false` window. Reach it from any component with
`useGpuixRequired()`:

```tsx
import { useGpuixRequired } from "@gpuix/react";

function Reveal() {
  const renderer = useGpuixRequired();
  return <div onClick={() => renderer.activateWindow?.()}>Show</div>;
}
```

Outside React, call it on the renderer that `createRenderer()` returned.

### Window controls

The desktop renderer exposes GPUI's native minimize, zoom, and fullscreen
operations. Reach them through `useGpuixRequired()` or the renderer returned by
`createRenderer()`.

```tsx
function WindowControls() {
  const renderer = useGpuixRequired();
  return (
    <div style={{ display: "flex", gap: 8 }}>
      <div onClick={() => renderer.minimizeWindow?.()}>Minimize</div>
      <div onClick={() => renderer.zoomWindow?.()}>Zoom</div>
      <div onClick={() => renderer.toggleFullscreen?.()}>Fullscreen</div>
    </div>
  );
}
```

`minimizeWindow()`, `zoomWindow()`, and `toggleFullscreen()` work on macOS,
Windows, Linux, and FreeBSD. `zoomWindow()` uses the platform's native zoom or
maximize operation. These methods are not available in the browser renderer.

### File picker

`promptForPaths()` opens the operating system's file picker. It resolves with
the selected absolute paths, or `null` when the user cancels.

```tsx
import { useGpuixRequired } from "@gpuix/react";

function AttachFiles() {
  const renderer = useGpuixRequired();

  const attach = async () => {
    const paths = await renderer.promptForPaths?.({
      files: true,
      multiple: true,
      prompt: "Attach",
    });
    if (paths) console.log(paths);
  };

  return <div onClick={attach}>Attach files</div>;
}
```

With no options, the picker selects one file. Set `directories: true` to select
directories instead. macOS can select files and directories in one prompt;
Windows and Linux require one kind per prompt. Invalid options and platform
picker failures reject. The browser method rejects because browsers return
`File` objects, not operating-system paths. An injected custom renderer can
omit this optional capability.

On the current Windows GPUI backend, the system dialog does not distinguish
cancellation from other `IFileDialog::Show` errors, so both resolve with
`null`. This needs a fix in GPUI before GPUIX can report those errors.

| Platform | `focus: false`                                              | `show: false` |
| -------- | ----------------------------------------------------------- | ------------- |
| macOS    | window orders in front without becoming key, like `open -g` | honored       |
| Windows  | `SW_SHOWNOACTIVATE`                                         | honored       |
| Linux    | **ignored**, the window opens focused                       | **ignored**   |

The process still gets a **Dock icon** on macOS. GPUI sets the regular
activation policy, so there is no menu-bar-agent mode yet. For a real
background daemon, run the app from a `launchd` agent in
`~/Library/LaunchAgents/`; launchd never activates the process.

### Let an agent drive the app

Make focus opt-in through the environment, so a human run behaves normally and
an agent run stays out of the way:

```tsx
render(<App />, {
  title: "Notes",
  focus: process.env.GPUIX_BACKGROUND !== "1",
});
```

```bash
bun app.tsx                      # you: window comes to the front
GPUIX_BACKGROUND=1 bun app.tsx   # agent: window opens behind your editor
```

`launch()` passes `env` straight through, so an agent script sets it once and
every screenshot, click, and assertion runs on a window that never interrupts
you:

```ts
import { launch } from "@gpuix/react/automation";

const app = await launch({
  command: "bun",
  args: ["app.tsx"],
  env: { GPUIX_BACKGROUND: "1" },
});

await app.getByTestId("bump").waitFor();
await app.getByTestId("bump").click();
await app.screenshot({ path: "tmp/after-click.png" });
await app.close();
```

Focus is the only thing that changes. **Automation does not need focus.**
`click()` hits the last painted bounds and `screenshot()` reads the GPU
surface, so both work while the window sits behind your editor, and even on a
`show: false` window that is not on screen at all.

```
  agent ──►  launch({ env: { GPUIX_BACKGROUND: '1' } })
                │
                ▼
           GPU window renders and paints without activation
                │
                ├──►  getByTestId(..).click()   ✓  hits the last painted bounds
                ├──►  screenshot({ path })      ✓  reads the GPU surface
                ├──►  fill() / press()          ✓  uses the live input pipeline
                └──►  close()

  you   ──►  keep typing, your editor stays frontmost the whole time
```

`fill()` and `press()` use the live GPUI window input pipeline. They work
without activating the desktop window. **Linux ignores `focus`**, so an agent
there still gets a focused window.

Prefer `createTestRoot()` when you can. It opens **no window at all**, so
nothing can steal focus and keyboard input works. Reach for `launch()` plus
`focus: false` when the check needs a real window, real GPU paint, or a real
process.

### flushSync

The root is a **concurrent root**, so React commits in a later microtask.
`flushSync` forces the render and the commit to finish before it returns, the
same as in `react-dom`.

```tsx
import { flushSync } from "@gpuix/react";

flushSync(() => setSidebarOpen(true));
```

It flushes **React only**, down to one `applyBatch` call. After it returns the
native retained tree is up to date, including styles and text.

It does **not** wait for GPUI. Layout and paint still happen on the next frame,
exactly like the browser paints after a DOM mutation. To see pixels, wait a
frame in the app, or call `renderer.flush()` in a test.

Use it when an ordering bug depends on the commit landing first: an unmount
before a remount, or a state change before you feed the next event.

## Debug frame overlay

GPUI paints frame-time stats into the window after layout. The overlay is not
a React element. A React FPS label would update every frame and cause more work.

```tsx
render(<App />, { title: "My App", debugFrameOverlay: "full" });
```

| Mode      | What you see                        |
| --------- | ----------------------------------- |
| `hidden`  | nothing (default)                   |
| `minimal` | last draw time, e.g. `8.3 MS`       |
| `full`    | `CUR`, `1%`, `10%`, `MAX`, `FRAMES` |

Or call the renderer:

```ts
renderer.setDebugFrameOverlay("full");
renderer.cycleDebugFrameOverlay();
renderer.resetDebugFrameOverlayStats();
renderer.getDebugFrameOverlay(); // 'hidden' | 'minimal' | 'full'
renderer.getDebugFrameOverlayStats();
// { currentMs, p90Ms, p99Ms, maxMs, frames, samples }
```

`p90Ms` is the overlay **10%** line. `p99Ms` is the **1%** line. Those are the slow tail.

The overlay shows **draw time**, not FPS. `8.3 MS` is about 120 Hz.

The chat example has a regression test for this: `examples/chat.perf.test.tsx`. It times mount, wheel draw, and sidebar clicks. It asserts p95, not every frame.

The default example suite excludes this hardware-timing test so shared CI runner variance does not fail functional checks. Run it explicitly on the target Mac:

On macOS, `THROTTLE=utility` restarts the process under `taskpolicy -c utility`. That pins work to E-cores. It is an **M1/M2 Air CPU** proxy, not Chrome 6x. GPU and RAM stay fast. `THROTTLE=background` is slower.

```bash
cd examples
THROTTLE=utility bun run test:perf
THROTTLE=utility bun --hot chat.tsx
```

## Hot reload

### 1. End the file with `render()`

```tsx
import { render } from "@gpuix/react";

function App() {
  return <div style={{ padding: 16 }}>hello</div>;
}

render(<App />, { title: "My App", width: 800, height: 600 });
```

Do **not** call `createRenderer()` or `init()` in this file. `bun --hot` re-runs
the whole entry on save. A second `init()` would open a second window.

### 2. Start the app with `bun --hot`

Prefer **`bun --hot`** over a plain `bun` or `tsx` run. Without `--hot`, a
save starts a second process. With it, `render()` remounts React on the same
window.

```bash
bun --hot app.tsx
```

### 3. Save the file

```
save .tsx  ►  bun re-evaluates the entry  ►  render() remounts React
                     │
                     ▼
              GpuixRenderer, window, GPU stay
```

The first `render()` creates the native host and stores it on `globalThis`.
Each save unmounts the React tree and mounts a new one on that same host.

**Stays:** window, GPU device, native `.node` addon, GPUI scroll physics.

**Resets:** `useState`, focus, React event handlers.

This is a remount, not React Refresh. Keeping hook state needs Bun to inject
`$RefreshReg$` during `--hot`. That transform exists on
`bun build --react-fast-refresh` only. Tracked in
[oven-sh/bun#40179](https://github.com/oven-sh/bun/issues/40179).

Native `.node` edits still need a rebuild. See [Developing the Rust side](#developing-the-rust-side).

On **macOS**, `startFrameLoop` calls `renderer.tick()` at a fixed rate (\~125fps by
default). Each tick drains only ready AppKit events and Core Foundation sources,
then returns without waiting for the next native wake. Bun timers, sockets, promises,
and PTY callbacks can run between ticks. Pass `{ frameMs }` to change the rate, and
call `.stop()` on the returned handle to end it.

A **runtime throw does not freeze the window.** The frame loop catches errors from
`tick()`, native event callbacks catch throws from React handlers, and `render()`
installs `uncaughtException` / `unhandledRejection` listeners so bun stays alive.
The window shows the stack and a **Reload** button that remounts the last
`render()` tree. Save under `bun --hot` also remounts. The process does not
exit.

On **Windows and Linux**, GPUI runs its normal blocking native event loop on one
dedicated Rust UI thread. `tick()` does not pump that loop. It only reports
whether the UI thread is still inside `Platform::run`. `startFrameLoop` still
creates a JavaScript timer so last-window-close can return false and `render()`
can `process.exit`, matching macOS. All platforms use GPUI's native platform,
window, renderer, input, scroll, clipboard, keyboard, and IME implementations.
The embedded macOS run-loop extension comes from the pinned GPUIX fork. CI runs
the full React and example test suites through DirectX on Windows.

<Info title="Important">
  On macOS, never drive `tick()` from a `setImmediate` loop. That spins at tens of thousands of
  ticks per second and burns **73% CPU on a completely idle app**, versus **1%** when
  paced.
</Info>
