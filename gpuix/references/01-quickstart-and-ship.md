# GPUIX — Creating, running, and shipping a GPUIX app

Verbatim sections quickstart–license from [gpuix.dev](https://gpuix.dev/index.md) (`index.md` lines 39–3406). Images and anchor links are relative to that page.

## In this file

- [Quickstart](#quickstart)
- [Examples](#examples)
- [Packages](#packages)
- [Building](#building)
- [Documentation](#documentation)
- [License](#license)

---

## Quickstart

Create an app from the official example. The command downloads only
`example-app/` and installs its dependencies. There is no repository clone,
native build, or Rust toolchain.

```bash
bunx @gpuix/cli new my-app
cd my-app
bun run dev
```

`@gpuix/react` pulls the native renderer for your platform. Edit `app.tsx` and
the running window remounts on save. Click and keyboard handlers switch to the
new tree without recreating the window.

Using Solid 1 instead? Start with the [Solid quick start](#solid-quick-start).

### Build from scratch

Install the packages directly when you do not want the example app:

```bash
bun add --exact @gpuix/react @gpuix/native react
bun add -d @types/react typescript
```

**Pin your adapter and `@gpuix/native` to the same exact version.** GPUIX is
still pre-1.0, so a new release can break either package. The adapter pulls
`@gpuix/native` with a version range, and that range can install a newer native
binary under an older adapter. Add both as direct dependencies. Upgrade them
together.

### 1. Point TypeScript at the GPUIX JSX types

**`jsxImportSource` is required.** Without it TypeScript uses DOM types, so
`<virtual-list>`, `<markdown>`, `<code>` and `style.hover` all fail to
typecheck.

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

### 2. Write the entry file

End the file with `render()`. That call creates the window, mounts React, and
starts the frame loop.

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

<Info title="Important">
  **Give every `<text>` a `color`.** GPUI does not inherit `color` from a
  parent, so text with no color paints **black** and disappears on a dark
  surface.
</Info>

### 3. Run it

```bash
bun --hot app.tsx
```

Use `bun --hot`, not plain `bun`. A save then remounts React on the same
window instead of opening a second one.

### 4. Ship a binary

```bash
bun build --compile app.tsx --outfile dist/app
./dist/app
```

The binary carries the renderer, so it runs with no Bun and no Node install.

For a smaller ship set, run the same React app on
[hermes-node](/guides/hermes) instead of Bun. That path is
**12 MB** plus a **22 MB** native sidecar. The steps are in that guide.

### 5. Wrap it in an app with an icon

A raw Mach-O has no Dock icon. Use
[cargo-packager](https://github.com/crabnebula-dev/cargo-packager) to wrap the
binary. Config: [Config](https://docs.rs/cargo-packager/latest/cargo_packager/config/struct.Config.html).
CLI: [docs.rs/cargo-packager](https://docs.rs/cargo-packager/latest/cargo_packager/).

```bash
cargo install cargo-packager --locked
```

Build an `.icns` from a 1024 PNG, then pack. Pass the `.icns`, not a 1024 PNG.
cargo-packager rejected a 1024 PNG with `No matching IconType`.

```bash
mkdir AppIcon.iconset
sips -z 16 16 icon-1024.png --out AppIcon.iconset/icon_16x16.png
sips -z 32 32 icon-1024.png --out AppIcon.iconset/icon_16x16@2x.png
sips -z 32 32 icon-1024.png --out AppIcon.iconset/icon_32x32.png
sips -z 64 64 icon-1024.png --out AppIcon.iconset/icon_32x32@2x.png
sips -z 128 128 icon-1024.png --out AppIcon.iconset/icon_128x128.png
sips -z 256 256 icon-1024.png --out AppIcon.iconset/icon_128x128@2x.png
sips -z 256 256 icon-1024.png --out AppIcon.iconset/icon_256x256.png
sips -z 512 512 icon-1024.png --out AppIcon.iconset/icon_256x256@2x.png
sips -z 512 512 icon-1024.png --out AppIcon.iconset/icon_512x512.png
sips -z 1024 1024 icon-1024.png --out AppIcon.iconset/icon_512x512@2x.png
iconutil -c icns AppIcon.iconset -o AppIcon.icns
```

**Bun** (one binary):

```json
{
  "productName": "My App",
  "version": "0.1.0",
  "identifier": "dev.example.app",
  "binariesDir": "dist",
  "outDir": "bundle",
  "binaries": [{ "path": "app", "main": true }],
  "icons": ["AppIcon.icns"],
  "formats": ["app"]
}
```

```bash
cargo packager --release --config packager.json
open "bundle/My App.app"
```

**Hermes** needs the `.node` next to the exe. List it as a **second binary**,
not a resource. Resources go in `Contents/Resources`. `dlopen` looks in
`Contents/MacOS`.

```json
{
  "binaries": [
    { "path": "gpuix-hermes", "main": true },
    { "path": "gpuix-native.darwin-arm64.node", "main": false }
  ]
}
```

`formats` is the host OS only:

| OS      | `formats`             | Output                  |
| ------- | --------------------- | ----------------------- |
| macOS   | `"app"`, then `"dmg"` | `.app`, optional `.dmg` |
| Windows | `"nsis"`              | setup `.exe`            |
| Linux   | `"appimage"`          | `.AppImage`             |

On this machine the Bun chat `.app` is **82 MB**. The Hermes counter `.app`
is **34 MB**.

### 6. Auto-update

Packaging does **not** turn on updates. The running app calls
`checkUpdate` on `@gpuix/native`. HTTP uses the same `reqwest_client` as
`<img>`. There is no second native addon.

Host on **GitHub Releases**. Create the release first. CI packs on each OS,
signs, and uploads the bundle plus its `.sig`. The app hits
`https://github.com/OWNER/REPO/releases/latest`. That rewrites to
`https://api.github.com/repos/OWNER/REPO/releases/latest`. The updater
reads `tag_name` and `assets`, then GETs the sibling `{name}.sig`.

Sign once:

```bash
cargo packager signer generate
```

Store the private key and its password as repo secrets
`CARGO_PACKAGER_SIGN_PRIVATE_KEY` and
`CARGO_PACKAGER_SIGN_PRIVATE_KEY_PASSWORD`. Put the **public** key in the app.

```tsx
import { checkUpdate } from "@gpuix/native";
import { render } from "@gpuix/react";
import { App } from "./app";

async function maybeUpdate() {
  const update = await checkUpdate("0.1.0", {
    endpoints: ["https://github.com/OWNER/REPO/releases/latest"],
    pubkey: "<public key from signer generate>",
  });
  if (update) await update.downloadAndInstall();
}

maybeUpdate();
render(<App />);
```

`https://github.com/OWNER/REPO` is the same endpoint.

Packager only builds the **host** OS. Run it on macOS, Linux, and Windows.
`--release` is the packager profile (look in `binariesDir` for a release
binary). It is not `cargo build --release`. Signing is automatic when those
two env vars are set. Source:
[cargo-packager CLI](https://docs.rs/cargo-packager/latest/cargo_packager/).

With `productName: "My App"`, `version: "0.1.0"`, and
`binaries: [{ "path": "app", "main": true }]`, packager writes:

| OS      | `formats`    | Files in `outDir` (`bundle/`)                                            |
| ------- | ------------ | ------------------------------------------------------------------------ |
| macOS   | `"app"`      | `My App.app`, then on sign `My App.app.tar.gz` + `My App.app.tar.gz.sig` |
| Linux   | `"appimage"` | `app_0.1.0_x86_64.AppImage` + `.sig`                                     |
| Windows | `"nsis"`     | `app_0.1.0_x64-setup.exe` + `.sig`                                       |

The macOS updater wants the **`.app.tar.gz`**, not the `.app` and not a
`.dmg`. Packager tars the `.app` only when it signs. Linux and Windows names
use the **binary stem** (`app`), not `productName`. NSIS arch is `x64`, not
`x86_64`. A missing sibling `.sig` is an error.

Create the GitHub release yourself, then pack and upload. `--clobber`
replaces an asset if CI retries. Do **not** upload a feed JSON.

```bash
# macOS
bun build --compile app.tsx --outfile dist/app
cargo packager --release --config packager.json
gh release upload v0.1.0 \
  "bundle/My App.app.tar.gz" \
  "bundle/My App.app.tar.gz.sig" \
  --clobber

# Linux
bun build --compile app.tsx --outfile dist/app
cargo packager --release --config packager.json
gh release upload v0.1.0 \
  bundle/app_0.1.0_x86_64.AppImage \
  bundle/app_0.1.0_x86_64.AppImage.sig \
  --clobber

# Windows
bun build --compile app.tsx --outfile dist/app.exe
cargo packager --release --config packager.json
gh release upload v0.1.0 \
  bundle/app_0.1.0_x64-setup.exe \
  bundle/app_0.1.0_x64-setup.exe.sig \
  --clobber
```

`downloadAndInstall()` replaces the packaged files. It does **not** relaunch.
Quit after it returns, or the next start uses the new app.

HTTPS is in the native crate. This works on **Bun** and **hermes-node**. It
does not exist in the browser wasm build. The repo must be **public**, or
GitHub will 404 the API. Optional: put a Cloudflare cache in front of
`api.github.com`. Same GitHub JSON. Not a custom schema.

### Start from the example app

[`example-app/`](https://github.com/remorses/gpuix/tree/main/example-app) is a complete todo app in one file, with `dev`,
`build`, `web:dev` and `typecheck` scripts already wired. Create a copy with
`bunx @gpuix/cli new my-app`.

<Image src="/_holocron/images/3dbc3469-todo-app.png" alt="The GPUIX todo example app" intrinsicWidth="1880" intrinsicHeight="1320" placeholder="data:image/webp;base64,UklGRjAAAABXRUJQVlA4ICQAAABwAQCdASoQAAsAAsBMJaWVuAGIAAD+9JFmMLL5NSzAw/0AAAA=" />

### Shell completions

Install completions for the `gpuix` command:

```bash
bun add -g @gpuix/cli
gpuix completions install
```

## Examples

| Example            | Run                                                                                        | What it shows                                                                                                                                                                               |
| ------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **todo**           | `bun run dev` in [`example-app/`](https://github.com/remorses/gpuix/tree/main/example-app) | The starting point: one file, a `<virtual-list>`, a native `<input>`, and an animated sidebar                                                                                               |
| **blurred window** | `bun run blurred-window`                                                                   | A macOS frosted-glass surface using GPUI's native vibrancy backdrop and transparent titlebar                                                                                                |
| **chat**           | `bun --hot chat.tsx`                                                                       | A GPUIX app: transparent titlebar, animated sidebar, per-thread transcripts, demo replies, composer, `<markdown>`                                                                           |
| **timeline**       | `bun --hot timeline.tsx`                                                                   | A video-editor timeline: clip dragging, edge trimming with snapping, playhead scrubbing, marquee selection, zoom under the pointer, and a two-axis pan with a frozen ruler and track column |
| **mail**           | `bun --hot mail.tsx`                                                                       | A Superhuman-style mail client: three panes, thread list, and a Framer newsletter                                                                                                           |
| **native-text**    | `bun --hot native-text.tsx`                                                                | The three native text components with a tab switcher                                                                                                                                        |
| **counter**        | `bun --hot counter.tsx`                                                                    | The smallest possible app: state, events, hover                                                                                                                                             |
| **diff**           | `bun --hot diff.tsx`                                                                       | A diff viewer composed from `<div>` and `<text>` in JS, for comparison                                                                                                                      |
| **web**            | `bun run web` from the repository root                                                     | The ChatGPT example rendered in a browser canvas with WebGPU                                                                                                                                |

The todo app lives in [`example-app/`](https://github.com/remorses/gpuix/tree/main/example-app) and is meant to be copied with `bunx @gpuix/cli new`.
The rest live in [`examples/`](https://github.com/remorses/gpuix/tree/main/examples). Those `bun --hot` commands need a clone of this repo and a local native build. They will not run against the published packages alone.

Or download a standalone **chat** build from the [GitHub release](https://github.com/remorses/gpuix/releases). No Bun or Rust install is required.

```bash
tar -xzf example-chat-aarch64-apple-darwin.tar.gz
./example-chat-aarch64-apple-darwin
```

The archive keeps the executable bit, so there is no `chmod` step. macOS may still block the unsigned binary the first time. Right-click the file, choose **Open**, and confirm.

On Windows, download `example-chat-x86_64-pc-windows-msvc.exe` and double-click it. On Linux, the file is `example-chat-x86_64-unknown-linux-gnu.tar.gz`.

The web example bundles the same React app and reconciler as the desktop chat
example. wasm-bindgen exposes mutations and event callbacks to the existing
retained tree and `GpuixView`, which run through GPUI's browser platform.

The web build needs nightly Rust and the matching wasm-bindgen CLI:

```bash
rustup toolchain install nightly --component rust-src --target wasm32-unknown-unknown
cargo install wasm-bindgen-cli --version 0.2.127 --locked
bun run web
```

The generated Wasm uses shared memory, so the page must be cross-origin
isolated. Production servers must send these headers on the **top-level
document**:

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

`require-corp` then constrains **cross-origin** subresources, which must supply
their own CORS or `Cross-Origin-Resource-Policy`. Serve the JavaScript and the
Wasm from the same origin as the document and nothing else is needed.

`bun run web` rebuilds the Wasm only when `packages/native/wasm` is missing.
After a Rust change, force it:

```bash
bun scripts/web.ts --rebuild
```

#### Hot reload in the browser

`bun run web` serves the example through Bun's frontend dev server, so an edit
to `examples/chat.tsx` arrives as a **React Fast Refresh** update. Components
swap in place and `useState` survives, which means the composer text, the
sidebar selection, and the scroll position all stay where they were. The GPUI
canvas is never re-created and the \~19 MB Wasm module is never re-fetched.

Fast Refresh only applies to a module whose exports are all components. Edit
anything else, such as the entry file, and Bun reloads the page instead. Both
paths are correct; the reload is only slower.

The Wasm half is a **singleton and must never re-evaluate**.
`WebGpuixRenderer::init` fails with `GPUIX web is already running` once its
thread-local app exists, and GPUI's browser platform appends its own canvas to
`<body>`. What protects it is not that it lives in `node_modules`; Bun bundles
it into the same client registry as your app. It is that Bun re-runs only the
**changed** module and then walks upward through its importers, so an unchanged
dependency stays evaluated and cached. Two rules follow:

- do not call `import.meta.hot.accept("./your-app", ...)` in the entry file.
  Bun runs an importer's dependency-accept callback **even when the imported
  module already self-accepted**, so that callback would remount the tree on top
  of a successful refresh and throw away every `useState`
- keep the `@gpuix/native` import in a module that can never become a Refresh
  boundary and is never explicitly accepted

The chat example puts a virtualized `<diff>` and a GFM table inside an assistant
turn, inside a scrolling transcript:

<Image src="/_holocron/images/30d6d0ba-chat-diff.png" alt="A diff and a markdown table inside a chat turn" intrinsicWidth="2560" intrinsicHeight="1600" placeholder="data:image/webp;base64,UklGRjIAAABXRUJQVlA4ICYAAABwAQCdASoQAAoAAsBMJaVefAGIAAD+8r+jFMBTotvfnK9eqVwAAA==" />

Markdown, code and a virtualized diff in one frame:

<Image src="/_holocron/images/fa215da6-showcase.png" alt="Markdown, code and diff rendered together" intrinsicWidth="2560" intrinsicHeight="1600" placeholder="data:image/webp;base64,UklGRiwAAABXRUJQVlA4ICAAAAAwAQCdASoQAAoAAsBMJaQAA3AA/vc816hE6JBpg0AAAA==" />

## Packages

- **`@gpuix/native`**: Rust bindings plus the framework-neutral TypeScript host runtime. It owns host types, mutation batching, renderer state, event routing, observers, native testing, and automation.
- **`@gpuix/native/host`**: host contracts, mutation helpers, renderer ownership, window observers, selection observation, and text search. Importing it does not load the `.node` addon.
- **`@gpuix/native/testing`**: the shared `TestRenderer` over the real `TestGpuixRenderer`.
- **`@gpuix/native/automation`**: the shared automation protocol, client, locators, and process launcher.
- **`@gpuix/react`**: the React reconciler and React components. It preserves its existing exports and re-exports shared testing, automation, search, and observer APIs.
- **`@gpuix/solid`**: the Solid 1 universal renderer, Solid primitives, motion, Select, Combobox, Tooltip, Bun preload, and build plugin.
- **`@gpuix/cli`** — `gpuix new` downloads `example-app/`, sets its published React dependency, and installs it as a standalone project.

Pin the selected adapter and `@gpuix/native` to the **same exact version**.
GPUIX is still pre-1.0. Breaking changes can land before v1. Upgrade them
together.

### Solid quick start

Install Solid and the official Solid adapter:

```bash
bun add --exact @gpuix/solid @gpuix/native solid-js
```

Use Solid's preserved JSX. The preload compiles application `.tsx` and `.jsx`
files for Solid's universal renderer and selects the reactive client runtime.

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "jsxImportSource": "@gpuix/solid",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true
  }
}
```

```toml
preload = ["@gpuix/solid/preload"]
```

```tsx
import { createSignal } from "solid-js";
import { render } from "@gpuix/solid";

function App() {
  const [count, setCount] = createSignal(0);
  return (
    <div style={{ padding: 24, backgroundColor: "#1a1a1a", height: "100%" }}>
      <div onClick={() => setCount((value) => value + 1)}>
        <text style={{ color: "#e2e2e2" }}>Count: {count()}</text>
      </div>
    </div>
  );
}

render(() => <App />, { title: "Solid GPUIX", width: 800, height: 600 });
```

Run it directly. No wrapper command or Vite configuration is required.

```bash
bun app.tsx
bun --hot app.tsx
```

For production `Bun.build`, pass the exported plugin:

```ts
import solidPlugin from "@gpuix/solid/bun-plugin";

await Bun.build({
  entrypoints: ["./app.tsx"],
  target: "bun",
  outdir: "./dist",
  plugins: [solidPlugin],
});
```

`@gpuix/solid` targets stable Solid 1.9. Its peer range is `>=1.9 <2`.

The full Solid adapter API is in the [Solid guide](/guides/solid).

## Building

This section is for **working on GPUIX itself**. To build an app with it, see
[Quickstart](#quickstart) instead. Installing the packages needs no Rust
toolchain and no submodule.

### Prerequisites

1. Rust toolchain
2. Node.js 18+
3. Xcode with Metal Toolchain (macOS)

```bash
# Install Metal Toolchain if needed
xcodebuild -downloadComponent MetalToolchain

# Install dependencies
bun install

# Check out the pinned GPUI fork
git submodule update --init --recursive

# Build native package
cd packages/native
bun run build

# Build React package
cd ../react
bun run build

# Build Solid package
cd ../solid
bun run build

# Run example (use tmux for long-running sessions)
cd ../../examples
bun --hot counter.tsx
```

## Documentation

See [AGENTS.md](https://github.com/remorses/gpuix/blob/main/AGENTS.md) for detailed architecture, communication flow, and contributing guide.

## License

[Apache-2.0](https://github.com/remorses/gpuix/blob/main/LICENSE)
