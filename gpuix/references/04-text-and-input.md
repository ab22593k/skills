# GPUIX — Native text input, selection, highlighting, markdown/code/diff

Verbatim sections text input–native text components from [gpuix.dev](https://gpuix.dev/index.md) (`index.md` lines 1680–2545). Images and anchor links are relative to that page.

## In this file

- [Text input](#text-input)
- [Text selection](#text-selection)
- [Text highlighting and search](#text-highlighting-and-search)
- [Native text components](#native-text-components)

---

## Text input

`<input>` and `<textarea>` use GPUI's platform input handler. They support a
native caret, text selection, IME composition, clipboard actions, undo/redo,
grapheme-safe deletion and mouse positioning.

```tsx
<textarea
  value={draft}
  placeholder="Ask anything"
  minRows={1}
  maxRows={8}
  onChange={(event) => setDraft(event.value ?? '')}
/>

<textarea
  value={draft}
  onChange={(event) => setDraft(event.value ?? '')}
  onSubmit={send}
/>
```

`Enter` inserts a newline in a `<textarea>`. Pass **`onSubmit`** to emit that
event on Enter instead; `Shift+Enter` still inserts a newline. An `<input>`
always emits `onSubmit` on Enter. The editor updates natively first, then
reports the complete value to React.
`value` changes can replace the native content, but keeping the same prop value
does not reject an edit like a browser-controlled input.

The focused caret stays solid during edits and then blinks every 500ms while
idle. It stops scheduling repaint frames on blur or while the window is
inactive. Override its colour through the shared native theme:

```tsx
<input theme={{ caret: "#22c55e" }} />
```

When the clipboard has no text, `Cmd+V` or `Ctrl+V` continues to `onKeyDown`
instead of disappearing inside the editor. Applications can then handle an
image-only or file-only clipboard themselves. Copied files also propagate even
when the operating system includes their paths as fallback text. Mixed text and
image clipboard content still pastes its text.

**`fontSize` and `lineHeight`** in `style` size each row. Without `lineHeight`,
the row uses GPUI's default leading, so a larger `fontSize` grows the box.
Pass `lineHeight` to set the row in pixels. `minRows` and `maxRows` multiply
that height. An explicit `height` still overrides both.

```tsx
<textarea
  value={draft}
  minRows={1}
  maxRows={8}
  style={{ fontSize: 14, lineHeight: 20 }}
  onChange={(event) => setDraft(event.value ?? "")}
/>
```

### Input in a search pill

`<input>` has **no default inner padding** and paints text at the top of its
box. A single-line input vertically centers its text when given extra height.
Set `padding` on the input style or on a parent wrapper. When the input has
`borderRadius`, text clips to the rounded shape automatically.

```tsx
<div
  style={{
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    height: 32,
    paddingLeft: 10,
    paddingRight: 4,
    borderRadius: 16,
    backgroundColor: "#1a1a22",
    borderWidth: 1,
    borderColor: "#ffffff14",
  }}
>
  <input
    value={query}
    onChange={(e) => setQuery(e.value ?? "")}
    style={{ flexGrow: 1, minWidth: 0, fontSize: 13, color: "#e8e8ed" }}
  />
</div>
```

## Text selection

Every text GPUIX paints is **selectable and copyable**, including text inside
`<code>`, `<diff>` and `<markdown>`. A drag that starts in a heading and ends
inside a fenced code block selects everything between; Cmd+C copies it joined in
document order.

There is nothing to opt into. A tap does not select. Only a drag does.
To opt _out_ — toolbars, buttons, line-number gutters — set
`userSelect: "none"`, which inherits like the CSS property:

```tsx
<div style={{ userSelect: "none" }}>
  <text>toolbar label, never selected</text>
</div>
```

<Image src="/_holocron/images/e502dfdf-selection.png" alt="Text selected across markdown blocks" intrinsicWidth="2560" intrinsicHeight="1600" placeholder="data:image/webp;base64,UklGRiwAAABXRUJQVlA4ICAAAACwAQCdASoQAAoAAsBMJaQAAxf+5/AAAP753D0nWsAAAA==" />

Read the selection from the renderer, or react when it changes:

```tsx
render(<App />, {
  onSelectionChange(event) {
    setCopied(event.value ?? "");
  },
});

renderer.getSelectedText(); // joined text, or null
renderer.clearSelection();
```

`onSelectionChange` is a **window-level** callback on `render()` / `createRoot()`,
the same attachment as `onKeyDown`. Text selection is app-wide, not per element.
It fires once when the selected ranges change, including a clear to empty
(`value` is then omitted). An unchanged frame does not fire.

The payload is a normal `EventPayload`. `value` is the joined selected text.

Selection works because each painted text element registers itself into a
per-frame registry in **paint order**, which is document order. A drag anchored
in one element resolves against that registry into per-element spans: partial in
the anchor and head, whole for everything between.

<Expandable title={<Markdown inline children="Why not one big text element, like Zed?" />}>
Zed's markdown selects continuously because its whole document is a single
element over one text model. GPUIX renders a _tree_ of text elements, so it
rebuilds that continuity at paint time instead. The mechanism is ported from
[Comet](https://github.com/zeronsh/comet) (MIT), which faced the same problem.
</Expandable>

## Text highlighting and search

The **`highlight` prop** paints a background wash behind matched text. Put it on
any element and it applies to that element's subtree, so the root searches the
window and a container searches only that container.

```tsx
<div highlight={{ query: "fox" }}>
  <text>the quick brown fox</text>
</div>
```

It reaches `<text>`, `<code>`, `<markdown>` and `<diff>` with no extra props,
because every string GPUIX paints goes through the same funnel.

### A find bar

`useTextSearch` owns the cursor and the count. `next` and `previous` are plain
event handlers, so nothing here needs an effect.

```tsx
import { useTextSearch } from "@gpuix/react";

function Find() {
  const [query, setQuery] = useState("");
  const search = useTextSearch({ query });

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1 }}>
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input value={query} onChange={(e) => setQuery(e.value ?? "")} />
        <text>
          {search.total === 0
            ? "No results"
            : `${search.active + 1}/${search.total}`}
        </text>
        <div onClick={search.previous}>
          <text>↑</text>
        </div>
        <div onClick={search.next}>
          <text>↓</text>
        </div>
      </div>

      <div {...search.props} style={{ flex: 1 }}>
        <Transcript />
      </div>
    </div>
  );
}
```

### Explicit ranges

When you already have offsets, from an LSP range or your own model, pass them
instead of a query. They are `[start, end)` in **UTF-16 code units**, the units
`indexOf` and `RegExp.exec` return.

```tsx
<div highlight={{ ranges: [[6, 11]], color: "#f43f5e55" }}>
  <text>Hello {name}!</text>
</div>
```

A pair that splits a surrogate pair is **rejected**, never snapped. Ranges index
retained text only; native elements build their strings in Rust, so use `query`
for those.

### Options

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

Pass an **array** to paint several at once, for example search matches plus a
persistent mention tint. Later entries draw on top.

### Matching rules

Matches are **non-overlapping** and leftmost-first. Case-insensitive matching
uses Unicode **lowercasing**, not full case folding, so `ﬀ` does not match `ff`.
A word boundary is any code point that is not Unicode Alphabetic, a digit,
or `_`.

A match never crosses a line, exactly like browser find. It **does** cross the
several host nodes React creates for one interpolated line, which matters more
than it sounds:

```tsx
// React makes 3 host text nodes here. `Hello Tommy` still matches.
<div highlight={{ query: "Hello Tommy" }}>
  <text>Hello {name}!</text>
</div>
```

The nearest declaration wins, so a nested `highlight` replaces its ancestor's
for that subtree.

**`userSelect: "none"` does not opt out of search.** A browser still finds that
text, so GPUIX still highlights it. Only element chrome, a code gutter or a diff
file header, is excluded.

<Expandable title={<Markdown inline children="Searching a virtual list" />}>
`<virtual-list>` never builds off-screen rows, so native can only see the
mounted window. Two things follow, and both are the app's job because the app
owns the row data.

**Count the matches yourself** with `findRanges`, which runs the same algorithm
as the native matcher on a string you give it.

**Say where your window starts**, as a count of **matches** above it, not a row
index. Without it native numbers the mounted rows from zero, `activeIndex` means
"the nth visible match", and the find cursor lands on the wrong row.

Both numbers travel together in `matches`, because supplying one without the
other is always wrong.

```tsx
import { findRanges, useTextSearch } from "@gpuix/react";

// One entry per row, so a prefix sum gives both numbers.
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

// search.next() moves the cursor; you do the scrolling
listRef.current.scrollToItem(rowOfMatch(search.active));
```

`findRanges` matches the native algorithm for the **same** string. Call it on
the same logical lines native paints: adjacent text nodes of one parent are one
line, and `<markdown>` paints inline runs rather than its source.
</Expandable>

<Expandable title={<Markdown inline children="Why a wash and not gpui's HighlightStyle" />}>
`HighlightStyle.background_color` is painted natively by gpui, but only with
square corners, and it cannot report the boxes it drew. GPUIX paints quads from
`range_rects`, the same helper selection and inline-code pills use, so a
soft-wrapped match is one box per visual row and `getPaintedHighlights()` can
assert the geometry without a screenshot. Zed's own editor paints search
highlights manually for the same reason.
</Expandable>

## Native text components

Three elements render text with Syntect syntax highlighting computed in
Rust. Colours come from a theme prop, so a late-arriving highlight recolours runs
without ever changing layout.

### `<code>`

A syntax-highlighted code block. One row per line at an exact line height, so the
block's height is known before highlighting runs.

It paints **no surface of its own**: no fill, border, radius, padding or language
header. `style` is the surface, so the card look is yours.

```tsx
<code
  code={source}
  language="typescript" // or path="src/app.ts" to detect from extension
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

<Image src="/_holocron/images/845aae1c-code.png" alt="A syntax-highlighted code block" intrinsicWidth="2560" intrinsicHeight="1600" placeholder="data:image/webp;base64,UklGRigAAABXRUJQVlA4IBwAAAAwAQCdASoQAAoAAsBMJaQAA3AA/veCyoWLJAAA" />

`fontFamily`, `fontSize`, `fontWeight`, `lineHeight` and `color` in `style` beat
the theme. Rows are a fixed height, so `fontSize` alone scales that height by the
theme's ratio; pass `lineHeight` to set it exactly.

Two things stay owned by the element: lines **never wrap**, and the block is its
own horizontal scroller. A long line pans on a horizontal wheel inside it, so
`whiteSpace` and `overflowX` in `style` do nothing.

For a language header, or any other chrome, wrap it in a `<div>` you own:

```tsx
<div
  style={{
    display: "flex",
    flexDirection: "column",
    borderRadius: 10,
    overflow: "hidden",
  }}
>
  <div style={{ padding: 6, backgroundColor: "#ffffff09" }}>
    <text style={{ fontSize: 12, color: "#a3a3a3" }}>{language}</text>
  </div>
  <code
    code={source}
    language={language}
    style={{ padding: 12, minWidth: 0 }}
  />
</div>
```

`<markdown>` is different: it keeps its own fenced-block card, because a document
renderer owns its layout. Tune that card with the `mdCode*` metrics.

### `<diff>`

A unified diff viewer. It **flows** with its parent by default, so a parent
list can be the only scroller. Collapsing a file removes its rows rather than hiding
them, so a collapsed 10k-line file costs one row.

Use `maxLines` to keep a long patch short. Show more fires `onShowMore`. Clear
`maxLines` in that handler to reveal the rest.

Pass `scroll` and a **bounded height** only for a dedicated full-window viewer.
That path uses GPUI's `list()` and virtualizes. Do not nest it inside another
scroller. See [Scrolling](#scrolling).

```tsx
<diff
  patch={unifiedPatch}
  wordDiff // highlight only the tokens that changed
  maxLines={open ? undefined : 24}
  collapsedPaths={["pnpm-lock.yaml"]}
  onShowMore={() => setOpen(true)}
  onToggleFile={(e) => toggle(e.value)}
  onLineClick={(e) => console.log(e.oldLine, e.newLine, e.value)}
/>
```

<Image src="/_holocron/images/f83cf7a1-diff.png" alt="A unified diff with word-level highlights" intrinsicWidth="2560" intrinsicHeight="1600" placeholder="data:image/webp;base64,UklGRiYAAABXRUJQVlA4IBoAAAAwAQCdASoQAAoAAsBMJaQAA3AA/vddynEAAA==" />

### `<markdown>`

GitHub-flavoured markdown: headings, lists, tables, block quotes, fenced code,
strikethrough, task lists, and autolinked bare URLs.

```tsx
<markdown source={readme} onLinkClick={(e) => open(e.value)} />
```

<Image src="/_holocron/images/d987569a-markdown.png" alt="Markdown with headings, lists, a table and a code fence" intrinsicWidth="2560" intrinsicHeight="1600" placeholder="data:image/webp;base64,UklGRiwAAABXRUJQVlA4ICAAAAAwAQCdASoQAAoAAsBMJaQAA3AA/vdh3rZDxwaiRZfAAA==" />

### Theming

All three take the same optional `theme` prop. Every field layers on top of the
built-in dark theme, so overriding one token leaves the rest alone.

```tsx
<code
  code={source}
  language="rust"
  theme={{
    appearance: "dark", // or 'light'
    accent: "#7c86ff",
    syntax: { keyword: "#f38ba8", string: "#a6e3a1" },
  }}
/>
```

**Layout numbers live in the theme too**, under `metrics`. Row heights, gutter
widths, paddings and the heading scale are props, not Rust constants, so tuning
the design is a React re-render and never a native rebuild.

```tsx
<diff
  patch={patch}
  theme={{
    metrics: {
      diffLineHeight: 26,
      diffGutterWidth: 48,
      mdHeadingSizes: [24, 19, 16, 14],
    },
  }}
/>
```

When `scroll` is on, `<diff>` virtualizes from these numbers without measuring,
so changing `diffLineHeight` also re-sizes the scroll model.

The same three components, retuned entirely from `metrics` with no rebuild:

<Image src="/_holocron/images/15fcd65a-metrics.png" alt="The components with enlarged metrics" intrinsicWidth="2560" intrinsicHeight="1600" placeholder="data:image/webp;base64,UklGRi4AAABXRUJQVlA4ICIAAAAwAQCdASoQAAoAAsBMJaQAA3AA/vcZ17a8QJmBKdW0JwAA" />

Languages bundled: Rust, TypeScript, TSX, JavaScript, JSX, Python, Go, JSON,
Bash, TOML, YAML, Markdown, HTML, CSS, C.
