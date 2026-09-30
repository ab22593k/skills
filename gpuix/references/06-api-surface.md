# GPUIX — Supported elements, images, events, styles, and current status

Verbatim sections supported elements–status from [gpuix.dev](https://gpuix.dev/index.md) (`index.md` lines 2546–3399). Images and anchor links are relative to that page.

## In this file

- [Supported Elements](#supported-elements)
- [Images and icons](#images-and-icons)
- [Supported Events](#supported-events)
- [Supported Styles](#supported-styles)
- [Status](#status)

---

## Supported Elements

| Element        | Description                                       |
| -------------- | ------------------------------------------------- |
| `div`          | Container with flexbox layout                     |
| `text`         | Text content, selectable                          |
| `code`         | Syntax-highlighted code block                     |
| `diff`         | Unified diff viewer. Flows by default             |
| `markdown`     | GitHub-flavoured markdown                         |
| `input`        | Native single-line text editor                    |
| `textarea`     | Native multiline, auto-growing text editor        |
| `virtual-list` | Long collections; only visible rows are built     |
| `img`          | Local, data URL, or http(s) raster or SVG images  |
| `svg`          | Tintable monochrome SVG icons from source or disk |
| `anchored`     | Positioned overlay                                |
| `canvas`       | Custom drawing (planned)                          |

## Images and icons

`<img>` takes a **filesystem path, data URL, or http(s) URL**. Resolve local
files with `fileURLToPath` or `path.join`, encode in-memory bytes as base64, or
pass a remote URL and let GPUI fetch it.

### `<img>`

`<img>` paints through GPUI's image element. It loads **PNG, JPEG, WebP, GIF,
SVG, BMP, TIFF, ICO, and Netpbm** from disk, data URLs, or http(s). SVG here is a
full-colour image, not a tintable icon.

```tsx
<img
  src={fileURLToPath(new URL("./photo.png", import.meta.url))}
  objectFit="cover"
  style={{ width: 240, height: 140, borderRadius: 12 }}
/>
```

```tsx
const src = `data:image/png;base64,${Buffer.from(pngBytes).toString('base64')}`

<img src={src} style={{ width: 240, height: 140 }} />
```

```tsx
<img
  src="https://example.com/avatar.png"
  objectFit="cover"
  style={{ width: 48, height: 48, borderRadius: 24 }}
/>
```

Set **both** `width` and `height`. GPUI fetches and decodes on a background
task. The tree does not wait. Without a definite size the box is empty until
decode, then jumps to the bitmap size.

Data URLs support every image format listed above. Base64 and percent-encoded
payloads are accepted. Remote URLs use the same GPUI image cache as disk files.
They are not written to a temp file.

`objectFit` matches CSS: `"contain"` (default), `"cover"`, `"fill"`,
`"scaleDown"`, or `"none"`. An empty `src` or a failed load shows a fallback
placeholder instead of crashing. A URL that is still loading paints an empty
box of the declared size. There is no spinner.

`borderRadius` clips the bitmap. GPUI paints the image with those corner
radii. A parent `overflow: "hidden"` wrapper does **not** clip an `<img>`
child. Put the radius on the image.

```tsx
<img
  src={avatarUrl}
  objectFit="cover"
  style={{ width: 32, height: 32, borderRadius: 16 }}
/>
```

### Live images from a buffer

A data URL still works, but it base64-encodes the bytes into the mutation JSON.
For a waveform, a canvas dump, or any frame you already have in memory, push
**raw bytes** through the `<img>` ref. That call skips JSON.

`setImage` takes encoded **PNG, JPEG, WebP, GIF, SVG, BMP, TIFF, ICO, or
Netpbm**. `setImagePixels` takes packed **RGBA**. Prefer pixels for a live
waveform. There is no PNG encode, and no JSON.

Call either from `useLayoutEffect` after mount. A later React `src` **change**
overwrites the pixels. Alpha is straight, not premultiplied.

There is **no density argument**. `width` and `height` on `setImagePixels` are
bitmap pixels. `style.width` and `style.height` are the layout box. On a retina
display, upload **2x** (or `devicePixelRatio`) the box size so GPUI does not
stretch one logical pixel into four screen pixels.

```tsx
import { createCanvas } from "canvas";
import { useLayoutEffect, useRef } from "react";
import type { ImgInstance } from "@gpuix/react";

function Waveform({ samples }: { samples: Float32Array }) {
  const img = useRef<ImgInstance>(null);

  useLayoutEffect(() => {
    const width = 1600;
    const height = 160;
    const canvas = createCanvas(width, height);
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "#1a1a2e";
    ctx.fillRect(0, 0, width, height);
    ctx.strokeStyle = "#5ca9ff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x = 0; x < samples.length; x++) {
      const y = height / 2 - samples[x]! * (height / 2 - 8);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    const { data } = ctx.getImageData(0, 0, width, height);
    img.current?.setImagePixels(width, height, data);
  }, [samples]);

  return <img ref={img} objectFit="fill" style={{ width: 800, height: 80 }} />;
}
```

`getImageData().data` is packed **RGBA**. That is what `setImagePixels` wants.
Do not use node-canvas `toBuffer('raw')`. That buffer is BGRA or ARGB, native
endian, and may include stride padding.

The [waveform example](/examples/waveform.tsx) writes the same RGBA layout by
hand, at 2x.

### `<svg>`

`<svg>` uses GPUI's **monochrome icon renderer**. Raw `source` works on desktop
and in the browser. Desktop apps can also use a local `src` path. The icon is
drawn as one shape and tinted with `style.color`.

For application icons, prefer **raw SVG source**. It works with both GPUIX
targets and lets a bundler embed each icon in the JavaScript bundle. Use `src`
only for a desktop app that intentionally ships loose asset files.

`src` is a filesystem path **or** a `data:image/svg+xml,…` URL. Vitest and some
Bun `import … with { type: 'file' }` bindings emit the data URL. GPUIX decodes
both.

`style.color` is required. Without it the icon does not paint. Prefer
`fill="#000"` or `stroke="#000"` in the file. `currentColor` in the SVG is not
the same as `style.color`.

#### Bun

Use Bun's [`text` loader](https://bun.sh/docs/bundler/loaders#text). The import
is a string containing the complete SVG, and `bun build` embeds it in the
bundle.

```tsx
import searchSvg from "./assets/icons/search.svg" with { type: "text" };

<svg source={searchSvg} style={{ width: 16, height: 16, color: "#b4b4b4" }} />;
```

The chat example builds every sidebar and composer icon from raw SVG source this
way.

#### Node.js

For supported Node.js releases, read the icon once relative to the module. A
`URL` keeps the path correct across operating systems and avoids `__dirname`.

```tsx
import { readFileSync } from 'node:fs'

const searchSvg = readFileSync(
  new URL('./assets/icons/search.svg', import.meta.url),
  'utf8',
)

<svg
  source={searchSvg}
  style={{ width: 16, height: 16, color: '#b4b4b4' }}
/>
```

Node.js also has [text modules](https://nodejs.org/api/esm.html#text-modules),
but they currently require `--experimental-import-text`. Prefer
[`readFileSync`](https://nodejs.org/api/fs.html#fsreadfilesyncpath-options) until
text imports no longer need a runtime flag.

## Supported Events

| Event            | Props                | Payload fields                                                                      |
| ---------------- | -------------------- | ----------------------------------------------------------------------------------- |
| Click            | `onClick`            | `x`, `y`, `button`, `clickCount`, `isRightClick`, `modifiers` — primary button only |
| Aux click        | `onAuxClick`         | `x`, `y`, `clickCount`, `isRightClick`, `modifiers` — non-primary buttons           |
| Mouse down       | `onMouseDown`        | `x`, `y`, `button`, `clickCount`, `modifiers`                                       |
| Mouse up         | `onMouseUp`          | `x`, `y`, `button`, `clickCount`, `modifiers`                                       |
| Mouse enter      | `onMouseEnter`       | `hovered`                                                                           |
| Mouse leave      | `onMouseLeave`       | `hovered`                                                                           |
| Mouse move       | `onMouseMove`        | `x`, `y`, `pressedButton`, `modifiers`                                              |
| Click outside    | `onMouseDownOutside` | `x`, `y`, `button`, `modifiers`                                                     |
| Key down         | `onKeyDown`          | `key`, `keyChar`, `isHeld`, `modifiers`                                             |
| Key up           | `onKeyUp`            | `key`, `keyChar`, `modifiers`                                                       |
| Focus            | `onFocus`            | —                                                                                   |
| Blur             | `onBlur`             | —                                                                                   |
| Scroll           | `onScroll`           | `deltaX`, `deltaY`, `precise`, `touchPhase`, `modifiers`                            |
| File drop        | `onFileDrop`         | `paths`, `x`, `y` — Unicode filesystem paths from Finder or the OS                  |
| Change           | `onChange`           | `value` — `<input>` and `<textarea>` only                                           |
| Submit           | `onSubmit`           | `value` — `<input>` always, `<textarea>` when `onSubmit` is set                     |
| Toggle file      | `onToggleFile`       | `value` (file path) — `<diff>` only                                                 |
| Show more        | `onShowMore`         | `value` (hidden line count) — `<diff>` only                                         |
| Line click       | `onLineClick`        | `value`, `oldLine`, `newLine` — `<diff>` only                                       |
| Link click       | `onLinkClick`        | `value` (URL) — `<markdown>` only                                                   |
| Selection change | `onSelectionChange`  | `value` (joined selected text) — window-level on `render()`                         |

A Finder or OS file drop lands on the hovered element that lists
**`onFileDrop`**. `paths` is an array of absolute Unicode filesystem paths.
`x` and `y` are the drop point in window pixels. An empty drop, or a drop
that contains a non-Unicode path, does not fire.

Put the listener on a **`div`**, **`text`**, **`img`**, **`svg`**, **`input`**,
**`textarea`**, **`code`**, **`markdown`**, **`diff`**, or **`anchored`**.
`<virtual-list>` does not take this event. Wrap it:

```tsx
<div
  onFileDrop={(event) => openFiles(event.paths ?? [])}
  style={{ width: 400, height: 300 }}
>
  <virtual-list estimatedItemHeight={24}>{rows}</virtual-list>
</div>
```

Keyboard and focus listeners create a persistent GPUI `FocusHandle`
automatically. A listener alone does not put a `div` in the Tab order; add
`tabIndex={0}` for that. Inputs and textareas already use tab index `0`.

A node that listens for both `onMouseDown` and `onMouseMove` **captures the
pointer**, like HTML [`setPointerCapture`](https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture).
`onMouseMove` and `onMouseUp` keep firing after the pointer leaves the hitbox,
leaves the parent, and leaves the window. A node with only `onMouseDown` /
`onMouseUp` does not capture, so a click still ends if you release outside.

Capture is armed by the **press itself**, so put all three listeners on the
element the user grabs:

```tsx
<div
  style={{ cursor: "grab", active: { cursor: "grabbing" } }}
  onMouseDown={(e) => beginDrag(e)}
  onMouseMove={(e) => moveDrag(e)}
  onMouseUp={endDrag}
/>
```

A full-window overlay mounted on the press cannot replace this. The overlay does
not exist yet when the press happens, so it never arms capture, and a release
past the window edge is lost. Only the pressed element receives moves while the
gesture runs, and only the hovered element receives them otherwise, so the cost
is one event per pointer move.

Capture arms on the **left** button only. A right-button drag is not captured,
so it ends when the pointer leaves the element.

`onClick` fires on primary-button mouse-up. Use **`onAuxClick`** for the others,
and read `event.isRightClick`. `onMouseDown` and `onMouseUp` see every
button through `event.button` (`0` left, `1` middle, `2` right).

## Supported Styles

CSS-like styling via the `style` prop:

```tsx
<div
  style={{
    display: "flex",
    flexDirection: "column",
    gap: 8,
    padding: 16,
    backgroundColor: "#3b82f6",
    borderRadius: 8,
  }}
>
  <div style={{ color: "#ffffff", fontSize: 18 }}>Hello GPUI!</div>
</div>
```

<Info title="Important">
  **GPUIX styles look like CSS but are not CSS.** A few differences trip
  everyone up on the first project:

- **`div` is block, not flex.** Set `display: "flex"` before using
  `flexDirection`, `gap`, `alignItems`, or `alignSelf`. Without it those
  props are silently ignored.
- **A flex child that must shrink needs `minWidth: 0`.** Same rule as CSS,
  but easier to miss because there is no browser DevTools to inspect.
- **No shorthand values.** `padding`, `margin`, and `border` take numbers.
  CSS strings like `"0 16px"`, `"1px solid #fff"`, or `calc()` are ignored.
- **`boxShadow` is a structured object**, not a CSS string. See below.
- **No `<button>`.** Use `<div onClick>` with `cursor: "pointer"`.
- **Do not nest `<text>` in `<text>`.** Adjacent `<text>` siblings merge
  into one line. A `<text>` child of another `<text>` is a nested div.
- **`<input>` has no default inner padding.** Set `padding` on the input
style, or pad the parent wrapper. The input clips to its own
`borderRadius` automatically.
</Info>

**Layout:** `display` (`"flex"` | `"grid"`), `flexDirection`, `flexWrap`, `flexGrow`, `flexShrink`, `flexBasis`, `alignItems`, `alignSelf`, `alignContent`, `justifyContent`, `gap`, `rowGap`, `columnGap`, `gridTemplateColumns`, `gridTemplateRows`, `gridColumnMin`, `gridRowMin`

**Sizing:** `width`, `height`, `minWidth`, `minHeight`, `maxWidth`, `maxHeight` — accepts pixels (number) or percentages (string like `"100%"`)

**Spacing:** `padding`, `paddingTop/Right/Bottom/Left`, `margin`, `marginTop/Right/Bottom/Left`

**Position:** `position` (`"relative"` | `"absolute"` | `"fixed"`), `top`, `right`, `bottom`, `left` — `"fixed"` lays out like `"absolute"`, because GPUI has no scrolling document to be fixed against

**Visual:** `background`, `backgroundColor`, `color`, `opacity`, `cursor`, `pointerEvents`, `borderRadius`, `borderTopLeftRadius`, `borderTopRightRadius`, `borderBottomLeftRadius`, `borderBottomRightRadius`, `borderWidth`, `borderTopWidth`, `borderRightWidth`, `borderBottomWidth`, `borderLeftWidth`, `borderColor`, `boxShadow`

### Cursors

`cursor` takes the CSS keyword. An unlisted keyword is ignored, like any other
invalid style value.

| Group    | Keywords                                                                                                                                                                               |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pointing | `default`, `auto`, `pointer`, `context-menu`, `not-allowed`, `no-drop`                                                                                                                 |
| Text     | `text`, `vertical-text`, `crosshair`                                                                                                                                                   |
| Dragging | `grab`, `grabbing`, `move`, `all-scroll`, `alias`, `copy`                                                                                                                              |
| Resizing | `col-resize`, `row-resize`, `ew-resize`, `ns-resize`, `nwse-resize`, `nesw-resize`, `n-resize`, `e-resize`, `s-resize`, `w-resize`, `ne-resize`, `nw-resize`, `se-resize`, `sw-resize` |

```tsx
<div style={{ cursor: 'grab', active: { cursor: 'grabbing' } }} />
<div style={{ cursor: 'col-resize' }} />
```

### Colors

Every color-bearing style field accepts the same string grammar. GPUIX native
uses `csscolorparser` 0.8.3 and accepts:

- named colors and `transparent`;
- 3/4/6/8-digit hex, with or without `#`;
- `rgb()` / `rgba()`, `hsl()` / `hsla()`, `hwb()` / `hwba()`, and
  `hsv()` / `hsva()`;
- `lab()`, `lch()`, `oklab()`, and `oklch()`;
- `none` components and the parser's limited relative-color `from` / `calc()`
  forms.

Standard comma and modern space/slash alpha forms work. Values are converted
to hard-clipped sRGB before GPUI paints them. Invalid strings are ignored for
that property; they do not reject the full style object.

### Linear gradients

`background` accepts GPUI's native **two-stop linear gradient**. Angles follow
CSS: `0` points up and values increase clockwise. Stop positions use `0` to `1`.

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

`colorSpace` is optional and defaults to `"srgb"`. GPUI also supports
`"oklab"`. It does not support radial, conic, repeating, or gradients with
more than two stops.

`hsv()`, `hsva()`, and `hwba()` are parser extensions rather than CSS Color 4
standard functions. `color()`, platform/dynamic colors, and numeric color
integers are not accepted.

Theme values can use the same modern grammar:

```tsx
const theme = {
  surface: 'oklch(18% 0.02 260)',
  accent: 'oklch(67.3% 0.182 276.935)',
  text: 'oklch(96% 0 0)',
}

<div style={{ backgroundColor: theme.surface, borderColor: theme.accent }}>
  <text style={{ color: theme.text }}>Hello GPUIX!</text>
</div>
```

Limited relative-color forms can derive a new color from a base value:

```tsx
<div
  style={{
    backgroundColor: "#bad455",
    borderColor: "oklch(from #bad455 calc(l - 0.15) calc(c * 0.7) h)",
  }}
/>
```

`boxShadow` accepts one structured shadow. Its fields are `offsetX`, `offsetY`,
`blurRadius`, `spreadRadius`, and `color`:

```tsx
<div
  style={{
    boxShadow: {
      offsetX: 0,
      offsetY: 4,
      blurRadius: 12,
      spreadRadius: 0,
      color: "#00000033",
    },
  }}
/>
```

**Overflow:** `overflow`, `overflowX`, `overflowY` — `"hidden"` clips content, `"scroll"` creates a native scrollable container with persistent scroll state

**Text:** `fontSize`, `fontFamily`, `fontWeight`, `textAlign`, `lineHeight`, `whiteSpace`, `textOverflow`, `lineClamp`, `textDecoration` (`"underline"` | `"line-through"` | `"none"`)

**Selection:** `userSelect` (`"text"` | `"none"`), `selectionColor` — both inherit down the tree

### Hover and active

`hover` and `active` are **nested style objects**. GPUI applies them natively
when the pointer is over the element or the mouse is down. There is no
JavaScript round trip.

```tsx
<div
  style={{
    backgroundColor: "#313244",
    borderRadius: 8,
    padding: 12,
    hover: { backgroundColor: "#45475a" },
    active: { backgroundColor: "#585b70" },
  }}
>
  Press
</div>
```

Nesting is one level deep. A `hover` object cannot contain another `hover` or
`active`.

They work on **every** element, including `<text>`, `<code>`, `<markdown>`,
`<diff>`, `<img>`, `<svg>` and the editors. The one exception is
`<virtual-list>`, whose `style` type rejects them: gpui's list has no
interactive identity to hold a hovered or pressed state, so put them on a
wrapping `<div>`.

> **Note: `white-space: pre` is not supported.** GPUI's text system only has `normal` (wraps) and `nowrap` (single line). To preserve newlines like HTML `<pre>`, split your text on `\n` in React and render each line as a separate `<text>` element in a flex column:
>
> ```tsx
> <div
>   style={{ display: "flex", flexDirection: "column", fontFamily: "Menlo" }}
> >
>   {code.split("\n").map((line, i) => (
>     <text key={i} style={{ whiteSpace: "nowrap" }}>
>       {line}
>     </text>
>   ))}
> </div>
> ```

> **Note: GPUI defaults text color to black, not white.** Unlike CSS, GPUI does not inherit `color` from parent elements. Every `<text>` element that doesn't set an explicit `color` style will render as black — invisible on dark backgrounds. Always set `color` on your text elements or on a parent `<div>` (which applies `text_color` to all children in that subtree via GPUI's `Styled` trait).

## Status

- [x] React reconciler with mutation-based protocol
- [x] Atomic `applyBatch()` mutation transport through napi-rs and wasm-bindgen
- [x] RetainedTree (Rust-side element storage)
- [x] Style mapping (CSS properties → GPUI style methods)
- [x] Mouse events (click, mouseDown, mouseUp, mouseMove, mouseEnter, mouseLeave)
- [x] Click outside (`onMouseDownOutside`)
- [x] Scroll wheel events with delta and touch phase
- [x] Scrollable containers (`overflow: "scroll"`) with persistent scroll state
- [x] Programmatic scroll API (`scrollTo`, `scrollToItem`, `scrollIntoView`, `getScrollOffset`)
- [x] Keyboard events (keyDown, keyUp) with focus management
- [x] Focus/blur events with automatic FocusHandle creation
- [x] GPU-backed test renderer with screenshot capture
- [x] Standalone build (pinned GPUI platform dependencies)
- [x] Native text input and multiline textarea
- [x] Image and SVG elements (`<img>`, `<svg>`), plus `setImage` / `setImagePixels` on `<img>` refs
- [x] Virtual lists (`<virtual-list>`)
- [x] Native text components (`<code>`, `<diff>`, `<markdown>`)
- [x] Cross-element text selection
- [x] Text highlighting and search (`highlight`, `useTextSearch`)
- [x] Headless Select, Combobox, and Tooltip
- [x] Native `hover` and `active` styles
- [x] Window title (`setWindowTitle`)
- [x] Native window controls (`minimizeWindow`, `zoomWindow`, `toggleFullscreen`)
- [x] Window chrome (`titlebarTransparent`, `windowBackground`, traffic-light position)
- [x] macOS menu bar with the standard shortcuts (`appName`)
- [ ] App-declared menus and menu callbacks
- [x] Background launch (`focus`, `show`, `activateWindow`)
- [x] Last window close quits the process
- [x] Runtime errors keep the macOS window alive and show a stack overlay
- [x] Debug frame overlay (`debugFrameOverlay` / `setDebugFrameOverlay`)
- [ ] Canvas element
- [ ] Multiple windows
- [x] JS remount under `bun --hot` (`render()` keeps the native window)
- [ ] React Refresh during `bun --hot` (needs a Bun runtime transform)
- [ ] Hot reload of the native `.node` addon. `bun run dev` rebuilds and restarts. Native modules cannot unload.
- [x] Native `motion.div` transitions with deterministic frame capture
- [x] `AnimatePresence` exit transitions for `motion.div`
