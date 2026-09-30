# GPUIX — Scrolling, nested-scroll rules, and virtual lists

Verbatim sections scrolling–virtual lists from [gpuix.dev](https://gpuix.dev/index.md) (`index.md` lines 1242–1679). Images and anchor links are relative to that page.

## In this file

- [Scrolling](#scrolling)
- [Virtual lists](#virtual-lists)

---

## Scrolling

Containers with `overflow: "scroll"` become natively scrollable. GPUI handles scroll physics, clipping, and offset persistence automatically.

Plain scroll containers still build every child. Use `<virtual-list>` below when the collection can grow large.

<Info title="Important">
  **Nested scrolling is not supported.** One parent may scroll. An inner
  `overflow: "scroll"`, `<virtual-list>`, or `<diff>` must not. GPUI gives both
  hitboxes the same wheel event, so the inner list steals the gesture.

Keep long inner content in that parent. Collapse it behind an **expandable**
(preview plus Show more) instead of giving the child its own viewport.

Horizontal overflow is the exception. `overflowX: "scroll"` on a wide child
(a code row, a table) does not steal the vertical wheel. GPUIX lays that
scroller out as a flex viewport with `minWidth: 0`. The wide child must not
shrink: set `flexShrink: 0` or a definite width. Swipe on **X** to pan.
A vertical wheel stays on the parent.
</Info>

```tsx
function Expandable({
  preview,
  children,
}: {
  preview: React.ReactNode;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {open ? children : preview}
      {!open && <div onClick={() => setOpen(true)}>Show more</div>}
    </div>
  );
}
```

```tsx
function ScrollableList() {
  return (
    <div style={{ height: 300, overflow: "scroll" }}>
      {items.map((item, i) => (
        <div key={i} style={{ height: 60, padding: 12 }}>
          {item.name}
        </div>
      ))}
    </div>
  );
}
```

Per-axis scrolling: use `overflowX: "scroll"` or `overflowY: "scroll"`.
`overflow: "scroll"` scrolls both axes at once from a single diagonal gesture,
like a browser.

A flex column stretches its children to the cross axis, so a two-axis container
needs its rows to state a width. Without one there is nothing to pan on **X**:

```tsx
<div
  style={{
    width: 260,
    height: 220,
    overflow: "scroll",
    display: "flex",
    flexDirection: "column",
  }}
>
  {rows.map((row) => (
    <div key={row.id} style={{ display: "flex", width: 810, flexShrink: 0 }}>
      {row.cells}
    </div>
  ))}
</div>
```

### Panes that must move together

A native scroll container cannot drive a **frozen header**. GPUI moves the
container on the wheel frame, and the JavaScript callback that would move the
header arrives a frame later, so the header tears away during a fast pan.

When two panes must stay locked to the pixel, own the offset in React: put one
`onScroll` listener on a non-scrolling parent, keep `scrollX` and `scrollY` in
state, and translate each pane's content with an absolutely positioned wrapper.
Zed does the same; the editor owns its scroll position and paints the gutter and
the text from it.

```tsx
function Pane({
  offsetX,
  children,
}: {
  offsetX: number;
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        flexGrow: 1,
        minWidth: 0,
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* An empty positioned box still takes hits, so opt it out. */}
      <div
        style={{
          position: "absolute",
          left: -offsetX,
          top: 0,
          pointerEvents: "none",
        }}
      >
        {children}
      </div>
    </div>
  );
}
```

Keep the moving subtree in a `memo` component whose props do not change during a
pan. The wheel then costs a handful of style mutations, not one per row. The
[timeline example](/examples/timeline.tsx) does this for a ruler, a track
column, and a clip grid.

For programmatic scroll, use a host ref. `scrollIntoView()` walks to the nearest
scroll parent. `scrollTo` and `scrollToItem` still exist on the renderer when
you already have an id.

```tsx
function ProgrammaticScroll() {
  const lastItem = useRef<PublicInstance>(null);

  return (
    <>
      <div style={{ height: 200, overflow: "scroll" }}>
        {items.map((item, i) => (
          <div key={i} ref={i === items.length - 1 ? lastItem : undefined}>
            {item}
          </div>
        ))}
      </div>
      <div onClick={() => lastItem.current?.scrollIntoView?.()}>
        Jump to last
      </div>
    </>
  );
}

renderer.scrollTo(elementId, x, y); // set offset directly
renderer.scrollToItem(elementId, index); // scroll child into view
renderer.scrollIntoView(elementId); // nearest scroll parent
renderer.getScrollOffset(elementId); // returns [x, y] or null
```

## Virtual lists

Use `<virtual-list>` for **long, variable-height collections** such as message lists. React and Rust retain every row, but GPUI only builds, lays out, and paints rows near the viewport.

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <virtual-list
      alignment="bottom"
      followTail
      estimatedItemHeight={180}
      style={{ flexGrow: 1, minHeight: 0 }}
    >
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
    </virtual-list>
  );
}
```

The list needs a **bounded height** or bounded flex space. Its direct children are rows and can contain any GPUIX host or custom element.

| Prop                  | Default | Purpose                                                        |
| --------------------- | ------: | -------------------------------------------------------------- |
| `alignment`           | `"top"` | Use `"bottom"` for chat-style initial positioning              |
| `followTail`          | `false` | Follow appended rows until the user scrolls away               |
| `overdraw`            |   `512` | Extra pixels built outside the viewport                        |
| `estimatedItemHeight` |    none | Height hint for unmeasured rows. **Required** with `itemCount` |

### How virtualization works

**React reconciliation stays normal.** The complete keyed child list crosses the mutation protocol and remains in Rust's retained tree. GPUIX defers only the expensive GPUI element construction, layout, and paint work.

```text
React Fiber + Rust RetainedTree    all row IDs, props, text, and events
                 │
                 ▼
          GPUI ListState          row count and measured height cache
                 │
                 ▼ visible indexes plus overdraw
          cx.processor            re-enters GpuixView after root render
                 │
                 ▼
          fresh BuildCtx          builds only the requested React subtree
                 │
                 ▼
       GPUI layout and paint      visible rows only
```

### Row heights

**Rows do not need equal heights, and you do not need to know them.** GPUI measures a row when it enters the viewport. `estimatedItemHeight` is a **hint for rows nothing has measured yet**, not a size contract.

```text
index:     0        1        2        3        4        5        6        7
       ┌────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
       │  hint  │  hint  │measured│measured│measured│  hint  │  hint  │  hint  │
       │  220px │  220px │  184px │  512px │   96px │  220px │  220px │  220px │
       └────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
           ▲                          ▲                          ▲
           │                          │                          │
     estimate only         real, variable heights          estimate only
                          (viewport plus overdraw)
```

The sum of that height cache is the scroll length, so a rough estimate only affects **scrollbar accuracy** before a row is visited. The measured height replaces the estimate automatically, and the scrollbar converges as you scroll.

When a retained descendant changes, GPUIX marks its direct row for remeasurement, so a streaming row grows correctly. Appending, removing, or reordering keyed rows keeps measurements for rows whose IDs did not change.

`estimatedItemHeight` is optional in children mode, where every row exists and can be measured. It is **required** with `itemCount`, because React never mounts the rows outside the window and native has no element to measure. Those indexes render as an empty box of the estimated height until React mounts the real row.

### Row boundaries

Each **direct host child** is one virtual row. Give every row a stable React key and one host root:

```tsx
<virtual-list style={{ height: 500 }}>
  {messages.map((message) => (
    <div key={message.id} style={{ paddingBottom: 24 }}>
      <Message message={message} />
    </div>
  ))}
</virtual-list>
```

A row can contain nested `<div>`, `<text>`, `<markdown>`, `<code>`, `<diff>`, `<input>`, and `<textarea>` elements. Focusable rows stay active when they move offscreen, so keyboard input and native editor state are preserved. Those children must not scroll. Nested scrolling is not supported; see [Scrolling](#scrolling).

### Chat tail behavior

Combine `alignment="bottom"` and `followTail` for a chat thread:

```tsx
<virtual-list
  alignment="bottom"
  followTail
  estimatedItemHeight={220}
  style={{ flexGrow: 1, minHeight: 0 }}
>
  {turns.map((turn) => (
    <ChatTurn key={turn.id} turn={turn} />
  ))}
</virtual-list>
```

The list follows new rows while the user is at the bottom. Scrolling upward pauses tail following. Returning to the bottom enables it again. A streaming final row is remeasured as its content grows.

### Scroll anchoring

The list is anchored on a **row index**, not on a pixel offset. In children mode React reconciles by key, so that index still lands on the same row after a prepend: the rows already on screen stay exactly where they are. A browser does the same, and calls it scroll anchoring.

One exception, also copied from the browser: a top-aligned list that is scrolled to the **very top** stays at the top, so a prepended row is visible.

```text
scrolled down                          pinned to the top
┌──────────────────┐                   ┌──────────────────┐
│ new row  (above) │  ◄── inserted     │ new row          │  ◄── inserted, visible
├──────────────────┤                   ├──────────────────┤
│ ░░ viewport ░░░░ │  stays put        │ ░░ viewport ░░░░ │  follows the insert
│ ░░░░░░░░░░░░░░░░ │                   │ ░░░░░░░░░░░░░░░░ │
└──────────────────┘                   └──────────────────┘
```

That is what a todo list or a feed wants: `setItems((current) => [fresh, ...current])` puts the new row on screen. A history pane that loads older pages while the user reads should use `alignment="bottom"` instead, so a page load never moves the text.

**With `itemCount`, the app owns the correction.** There is no key to reconcile against, so the index is all there is. Prepending shifts every row down one slot, and the anchor keeps pointing at the old number, so the content slides by exactly the number of rows you inserted. Move `windowStart` by the same amount:

```tsx
const prepend = (fresh: Row) => {
  setRows((current) => [fresh, ...current]);
  // The anchor is an index. One new row above the window means every existing
  // row moved down one, so the window has to move with it.
  setWindowStart((start) => (start === 0 ? 0 : start + 1));
};
```

Leave `windowStart` at `0` alone; the list is pinned to the top there and the new row should be visible.

### Programmatic scrolling

Use a ref to call the same renderer scroll methods as a plain scroll container:

```tsx
function Results({ rows }: { rows: Result[] }) {
  const renderer = useGpuixRequired();
  const listRef = useRef<{ id: number } | null>(null);

  const reveal = (index: number) => {
    if (listRef.current) {
      renderer.scrollToItem?.(listRef.current.id, index);
    }
  };

  return (
    <>
      <virtual-list ref={listRef} style={{ height: 400 }}>
        {rows.map((row) => (
          <ResultRow key={row.id} row={row} />
        ))}
      </virtual-list>
      <div onClick={() => reveal(rows.length - 1)}>Reveal latest</div>
    </>
  );
}
```

`scrollTo`, `scrollToItem`, and `getScrollOffset` all support virtual lists.

On a virtual list, `scrollToItem` takes an optional **pixel offset** and the
list reports its logical anchor:

```tsx
renderer.scrollToItem(listId, index, offsetInItem); // offset in px, may be negative
renderer.getListScrollTop(listId); // [itemIndex, offsetInItemPx, viewportHeightPx] or null
```

A **negative offset anchors the viewport top above the row**, and the next
layout resolves it against real measured heights. That is the tool for
infinite-scroll history: while the reader waits in a loading row, read
`getListScrollTop`, commit the fetched page, then re-anchor on the message
that was under the loading row with a negative offset. The message stays at
the same pixel while the new rows are measured above it —
`examples/infinite-chat.tsx` is the worked example.

An `itemIndex` equal to the item count is gpui's **at-end sentinel**: a
bottom-aligned list resting at its very end. A reader waiting at a trailing
loading row usually sits there, and the viewport height in the same tuple is
what converts that into a position relative to the trailing rows
(`EDGE_HEIGHT - viewportHeight` in the example).

Virtual-list `scrollToItem` calls are applied on the **next render, after
that frame's child splice**, so an index computed against a just-committed
child list is never shifted twice.

### Performance model

| Work                  | Plain scroll container | `<virtual-list>` children     | `<virtual-list>` + `itemCount`        |
| --------------------- | ---------------------- | ----------------------------- | ------------------------------------- |
| React Fiber nodes     | All rows               | All rows                      | Visible window                        |
| Rust retained nodes   | All rows               | All rows                      | Visible window                        |
| GPUI row construction | All rows               | Visible rows plus overdraw    | Visible rows plus overdraw            |
| Layout and paint      | All rows               | Visible rows plus overdraw    | Visible rows plus overdraw            |
| Height metadata       | None                   | One lightweight entry per row | One lightweight entry per logical row |

The children form still creates every React child, so a 10,000-row `turns.map` is slow to mount. Pass `itemCount` and `windowStart` and render only that slice to mount a window too. Collections with millions of rows still need application-level paging or a data-owning native element.

### Keep scroll fast

A wheel event notifies the window view. GPUI then rebuilds the **visible**
rows and Taffy lays them out again. Draw time is the cost of those rows, not
the length of the list.

Put a long list on `<virtual-list>`. Keep `overdraw` near one extra
viewport. Put fat content in one native node (`<markdown>`, `<code>`, `<diff>`),
not a tree of React spans.

The host `<virtual-list>` still retains every React child. Pass `itemCount`,
`estimatedItemHeight` and `windowStart`, then render only that window, so mount
does not create every row. Native ignores `itemCount` when the estimate is
missing, so a jump cannot collapse unmounted rows to height 0.

There is **no `VirtualList` wrapper component**. The window is app state:
only the app knows when it must widen, for example when a filter grows
`itemCount` without any scroll. Keep `start` in `useState`, move it from
`onVisibleRange`, and slice around it.

```tsx
const WINDOW = 40;

const Transcript = memo(function Transcript({ turns }: { turns: Turn[] }) {
  const [start, setStart] = useState(0);
  const end = Math.min(turns.length, start + WINDOW);
  return (
    <virtual-list
      itemCount={turns.length}
      windowStart={start}
      estimatedItemHeight={220}
      style={{ flexGrow: 1, minHeight: 0 }}
      onVisibleRange={(event) =>
        setStart(Math.max(0, Math.floor(event.startIndex ?? 0) - WINDOW / 4))
      }
    >
      {turns.slice(start, end).map((turn) => (
        <ChatTurn key={turn.id} turn={turn} />
      ))}
    </virtual-list>
  );
});

function ChatApp() {
  const [collapsed, setCollapsed] = useState(false);
  const [turns, setTurns] = useState(initialTurns);
  return (
    <div style={{ display: "flex", flexDirection: "row", height: "100%" }}>
      <Sidebar collapsed={collapsed} onCollapse={() => setCollapsed(true)} />
      <Transcript turns={turns} />
      <Composer
        onSend={(text) => setTurns((current) => [...current, { text }])}
      />
    </div>
  );
}
```

`turns` is a new array only when a message arrives. Sidebar and draft updates
leave that reference alone, so `memo` skips the map. The chat example uses
this pattern.

`overflowX: "scroll"` on a wide child must not steal the vertical wheel.
GPUIX sets `restrict_scroll_to_axis` on that path. Native
`overflow_x_scroll()` must call the same method.

Turn on `debugFrameOverlay: 'full'` while you scroll. The overlay is **draw
time**. `8.3 MS` is about 120 Hz.

### Pannable surfaces must cull

`<virtual-list>` is the only thing that virtualizes. A surface where **you** own
the offset — a timeline, a node graph, a map — places its children absolutely,
so GPUI builds and lays out **every** retained child on every frame. Nothing
skips them for you.

`memo` and culling fix different halves, and only one of them is the draw:

```
memo(Layer)  ►  cuts React work and the applyBatch mutations
cull in JS   ►  cuts GPUI build, Taffy layout, and paint
```

You already know the offset, so the visible window is a `useMemo` away:

```tsx
const visible = useMemo(() => {
  const from = scrollX / pxPerSecond;
  const to = (scrollX + viewportWidth) / pxPerSecond;
  return clips.filter(
    (clip) => clip.start <= to && clip.start + clip.duration >= from,
  );
}, [clips, scrollX, pxPerSecond, viewportWidth]);
```

The timeline example measures both, on 3,259 clips across 26 tracks:

| Wheel pan, one full frame | p50        |
| ------------------------- | ---------- |
| Culled                    | **7.7 ms** |
| `memo` only, no culling   | **92 ms**  |

<Info title="Important">
  A perf sample must include `renderer.flush()`. Without it you time the React
  update and none of the GPUI build, layout, and paint that follows. The
  `memo`-only number above looks like **0.6 ms** if you forget.
</Info>
