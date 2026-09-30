# GPUIX — Accessibility, focus and keyboard nav, headless controls, motion.div

Verbatim sections accessibility–native animations from [gpuix.dev](https://gpuix.dev/index.md) (`index.md` lines 1766–1241). Images and anchor links are relative to that page.

## In this file

- [Accessibility](#accessibility)
- [Focus and keyboard navigation](#focus-and-keyboard-navigation)
- [Headless controls](#headless-controls)
- [Native animations](#native-animations)

---

## Accessibility

GPUI talks to the **macOS AX tree**, Windows UIA, and Linux AT-SPI through
AccessKit. GPUIX maps React props onto that API. A node is in the tree only
when it has **both** a GPUI id (always set) and a **role**.

Prop names match React DOM. Role **values** are ARIA tokens, not AccessKit
PascalCase. `"none"` and `"presentation"` produce no node.

```tsx
<div
  role="button"
  aria-label="Delete note"
  aria-description="Removes this note"
  aria-id="notes.delete"
  onClick={remove}
>
  Delete
</div>
```

| Prop               | GPUI / AccessKit                          |
| ------------------ | ----------------------------------------- |
| `role`             | `.role(Role::…)`                          |
| `aria-label`       | accessible name                           |
| `aria-description` | extra description after name, role, value |
| `aria-id`          | `AXIdentifier` / UIA AutomationId         |
| `aria-expanded`    | expanded state                            |
| `aria-selected`    | selected state                            |
| `aria-valuetext`   | string value                              |
| `aria-level`       | heading level                             |

Native defaults, so common elements are not silent:

| Element      | Default role         | Name / value                |
| ------------ | -------------------- | --------------------------- |
| `<text>`     | `Label`              | content as `aria-valuetext` |
| `<input>`    | `TextInput`          | `value` and `placeholder`   |
| `<textarea>` | `MultilineTextInput` | `value` and `placeholder`   |
| `<img>`      | `Image`              | `alt` as `aria-label`       |

An explicit `role` wins over those defaults. A clickable `div` is **not** a
button until you set `role="button"`. `onClick` registers AccessKit `Click`,
so VoiceOver Press fires the same JS `click` handler.

The browser / wasm renderer has no AccessKit adapter. These props are
no-ops there.

## Focus and keyboard navigation

Focus is a **native GPUI concept**. GPUIX connects stable React element IDs to
persistent `gpui::FocusHandle` values, so focus survives React rerenders:

```text
React <div tabIndex={0}>
            │
            ▼
Retained element ID ► persistent gpui::FocusHandle ► keyboard/action dispatch
            ▲
            │
      React rerenders
```

Inputs and textareas are tab stops automatically. Add `tabIndex` to a `div` when
it should participate in explicit focus traversal:

```tsx
<div
  tabIndex={0}
  onFocus={() => setActive(true)}
  onBlur={() => setActive(false)}
  onKeyDown={(event) => {
    if (event.key === "enter") submit();
  }}
>
  Submit
</div>
```

| Prop            | Behavior                                                           |
| --------------- | ------------------------------------------------------------------ |
| `tabIndex={0}`  | Joins the normal focus traversal order                             |
| `tabIndex={n}`  | Uses `n` as its GPUI tab-order index                               |
| `tabIndex={-1}` | Skipped by focus traversal, but focusable by click or renderer API |
| `autoFocus`     | Takes focus once, when its native focus handle is created          |

### Element keyboard callbacks

`onKeyDown` fires for the focused element and then for ancestors that declare
`onKeyDown`, following GPUI's focus dispatch path. `onKeyUp` follows the same
path when the key is released. Adding either callback creates the element's
native focus handle.

```tsx
<div
  autoFocus
  tabIndex={0}
  onKeyDown={(event) => {
    console.log(event.key, event.keyChar, event.modifiers, event.isHeld);
  }}
  onKeyUp={(event) => {
    console.log(`${event.key} released`);
  }}
>
  Focused target
</div>
```

GPUI dispatches matching key actions before raw keyboard callbacks. If an
action consumes the key, `onKeyDown` does not fire. GPUIX does not bind `Tab` or
`Shift+Tab`, so both reach element callbacks. Editors and terminals can send
them directly to their input backend.

### Renderer keyboard callbacks

Pass `onKeyDown` or `onKeyUp` to `render()` for an opt-in window-level listener.
The renderer callback fires after element callbacks for raw keys that no GPUI
action consumed. It receives the renderer as its second argument:

```tsx
render(<App />, {
  onKeyDown(event, renderer) {
    if (event.key !== "tab") return;
    if (event.modifiers?.shift) renderer.focusPrevious?.();
    else renderer.focusNext?.();
  },
});
```

These callbacks observe native events. They do not expose GPUI's propagation
control, so they cannot cancel or stop the native event.

Do not also call `focusNext` from an element `onKeyDown`. Both move focus, and
the window listener cannot stop the native event, so Tab would jump twice.

### Imperative focus

`focusNext()` and `focusPrevious()` map directly to GPUI's
`window.focus_next()` and `window.focus_prev()`.
`focusNextWithin(id)` / `focusPreviousWithin(id)` wrap inside that subtree.
`getFocusedElementId()` returns the host id, or `null`. Browser focus requests made
while WebGPU opens are queued and applied after the first focus handles exist. If
several requests arrive before that render, the latest request wins.

Use a ref for imperative focus:

```tsx
const buttonRef = useRef<{ id: number }>(null);

function focusButton() {
  if (buttonRef.current) renderer.focusElement(buttonRef.current.id);
}

<div ref={buttonRef} tabIndex={-1}>
  Focused on demand
</div>;
```

Adding `onKeyDown`, `onKeyUp`, `onFocus`, or `onBlur` creates a persistent focus
handle. Add `tabIndex` as well when the element must be reachable through focus
traversal. Removing `tabIndex` removes the element from that order.

## Headless controls

The built-in controls are **unstyled primitives**, not a fixed component
library. Use them like Radix primitives in shadcn: import a primitive namespace,
wrap and style it in a local file, then import those local components throughout
the app.

```text
@gpuix/react/select ► components/ui/select.tsx ► application screens
  native behavior       local styles/variants       product-specific use
```

Each primitive has a dedicated namespace entry point:

| Import                  | Main parts                                          |
| ----------------------- | --------------------------------------------------- |
| `@gpuix/react/select`   | `Root`, `Trigger`, `Value`, `Content`, `Item`       |
| `@gpuix/react/combobox` | `Root`, `Input`, `Content`, `List`, `Item`, `Empty` |
| `@gpuix/react/tooltip`  | `Provider`, `Root`, `Trigger`, `Content`            |
| `@gpuix/react/floating` | `FloatingLayer`, `renderSlot`                       |

### Build a local Select

Create `components/ui/select.tsx`. This file is application code, so it can be
copied and changed without waiting for GPUIX to add a theme option:

```tsx
import * as React from "react";
import * as SelectPrimitive from "@gpuix/react/select";

export const Select = SelectPrimitive.Root;
export const SelectValue = SelectPrimitive.Value;
export const SelectGroup = SelectPrimitive.Group;

export const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  SelectPrimitive.SelectTriggerProps
>(({ style, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    {...props}
    style={(state) => ({
      width: 220,
      height: 36,
      padding: 8,
      backgroundColor: state.open ? "#334155" : "#1e293b",
      borderRadius: 8,
      ...(typeof style === "function" ? style(state) : style),
    })}
  />
));

export const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  SelectPrimitive.SelectContentProps
>(({ style, ...props }, ref) => (
  <SelectPrimitive.Content
    ref={ref}
    sideOffset={6}
    {...props}
    style={{
      width: 220,
      maxHeight: 240,
      overflowY: "scroll",
      padding: 4,
      backgroundColor: "#0f172a",
      borderRadius: 8,
      ...style,
    }}
  />
));

export const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  SelectPrimitive.SelectItemProps
>(({ style, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    {...props}
    style={(state) => ({
      padding: 8,
      opacity: state.disabled ? 0.4 : 1,
      backgroundColor: state.highlighted
        ? "#334155"
        : state.selected
          ? "#1e3a5f"
          : "#0f172a",
      ...(typeof style === "function" ? style(state) : style),
    })}
  />
));
```

Pass **`items`** on `Root` when `SelectValue` should show a label while the
menu is closed. Keyboard nav reads the mounted `SelectItem` children. A styled
wrapper around `Item` is fine. Without `items`, `SelectValue` shows the raw
value.

```tsx
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './components/ui/select'

const models = [
  { value: 'sonnet', label: 'Sonnet' },
  { value: 'opus', label: 'Opus' },
]

<Select items={models} value={model} onValueChange={setModel}>
  <SelectTrigger>
    <SelectValue placeholder="Select a model" />
  </SelectTrigger>
  <SelectContent>
    <SelectGroup>
      {models.map((item) => (
        <SelectItem key={item.value} value={item.value}>
          {item.label}
        </SelectItem>
      ))}
    </SelectGroup>
  </SelectContent>
</Select>
```

The trigger participates in normal tab navigation. Opening the Select focuses
its content. `Up`, `Down`, `Ctrl+P`, `Ctrl+N`, `Enter`, and `Escape` control the
menu. Closing it restores focus to the trigger. Disabled items are skipped.

GPUI does not bubble clicks. Use `asChild` when a styled row paints the item
fill, so that row becomes the real hit target:

```tsx
<SelectItem value="opus" asChild>
  <MenuRow>Claude Opus 4.6</MenuRow>
</SelectItem>
```

The child must forward its ref and host props. `ComboboxItem` supports the same
pattern.

### Style Combobox and Tooltip the same way

Start their local files from namespace imports too:

```tsx
// components/ui/combobox.tsx
import * as ComboboxPrimitive from "@gpuix/react/combobox";

// components/ui/tooltip.tsx
import * as TooltipPrimitive from "@gpuix/react/tooltip";
```

The application still uses compound components, not one large configuration
object:

```tsx
<ComboboxPrimitive.Root items={["Next.js", "SvelteKit", "Astro"]}>
  <ComboboxPrimitive.Input style={{ width: 220, height: 36, padding: 8 }} />
  <ComboboxPrimitive.Content style={{ width: 220 }}>
    <ComboboxPrimitive.Empty>No frameworks found.</ComboboxPrimitive.Empty>
    <ComboboxPrimitive.List>
      {(item) => (
        <ComboboxPrimitive.Item key={item} value={item}>
          {item}
        </ComboboxPrimitive.Item>
      )}
    </ComboboxPrimitive.List>
  </ComboboxPrimitive.Content>
</ComboboxPrimitive.Root>
```

```tsx
<TooltipPrimitive.Provider delayDuration={350}>
  <TooltipPrimitive.Root>
    <TooltipPrimitive.Trigger asChild>
      <div tabIndex={0} style={{ padding: 8 }}>
        Copy
      </div>
    </TooltipPrimitive.Trigger>
    <TooltipPrimitive.Content side="top" sideOffset={6}>
      Copy message
    </TooltipPrimitive.Content>
  </TooltipPrimitive.Root>
</TooltipPrimitive.Provider>
```

Combobox uses the native input for text editing, IME, clipboard, and focus.
Tooltip `asChild` preserves the child ref and merges trigger behavior into that
host element. All floating content uses GPUI's deferred `anchored()` layer,
snaps inside the window, and occludes controls behind it.

### Overlay menus

Menus, tooltips, and dialogs must use **`SelectContent`**, **`ComboboxContent`**,
or `<anchored deferred>`. Those paint in a later pass, on top of
`<virtual-list>` and the rest of the page.

A `position: "absolute"` card that overflows out of the composer sits **under**
the virtual list. The list paints after the composer, so you still see the
markdown through the menu, and clicks hit the text behind it.

```tsx
<Select
  items={[{ value: "flash", label: "DeepSeek V4 Flash" }]}
  value={model}
  onValueChange={setModel}
>
  <div style={{ position: "relative" }}>
    <SelectTrigger>
      <SelectValue />
    </SelectTrigger>
    <SelectContent
      side="top"
      sideOffset={4}
      style={{ backgroundColor: "#232323" }}
    >
      <SelectItem value="flash">DeepSeek V4 Flash</SelectItem>
    </SelectContent>
  </div>
</Select>
```

Give every overlay an **opaque** fill (`#232323`, not `#23232399`).
`FloatingLayer` defaults to `#1A1A1A`. Item rows should use the same solid
color, or a solid hover color. A `#00000000` child on a blurred window punches
through Metal to the desktop.

`FloatingLayer` copies uniform and per-corner border radii to its anchored
surface, so rounded Select, Combobox, and Tooltip content does not show square
corners behind it. It also puts `visibility` and `opacity` on that outer surface
so the fallback fill follows them without multiplying nested opacity.
`pointerEvents: "none"` disables the anchored occluder. Backgrounds, borders,
shadows, overflow, and layout remain on the inner content to avoid double paint
or changed popup geometry.

A `div` that paints a fill, or that is positioned, blocks clicks and hovers
behind it. The **wheel still passes**, so a pannable canvas can place its items
absolutely and keep panning.

Set **`pointerEvents: "auto"`** on an element that must swallow the wheel too,
like a modal backdrop. `<anchored>` occludes by default and has its own
`occlude` prop, so menus and tooltips need neither.

<Info title="Important">
  The wheel does not bubble the way DOM events do. GPUI hit-tests one flat list
  of painted boxes, so the wheel reaches **any** scroller behind the element,
  not only an ancestor. An absolute card floating over an unrelated scroll pane
  will scroll that pane. Give a real overlay `pointerEvents: "auto"`.
</Info>

`pointerEvents: "none"` means the element inserts **no hitbox**, so it blocks
nothing behind it. It does not disable the listeners on that same element, and
it does not inherit, so children keep their own hitboxes.

A filled child of a click target (switch thumb, radio dot, check icon) needs
**`pointerEvents: "none"`**, or it eats the parent's click. For Select and
Combobox rows, use the item primitive's `asChild` prop instead.

### Measure an element

`getElementBounds(id)` returns the last painted box, or `null` if that node did
not paint. It works on the live `GpuixRenderer` and on the test renderer.
Bounds are recorded during **paint**, so read them after a frame, not in the
same commit as mount.

```tsx
const box = renderer.getElementBounds?.(ref.current.id);
// { x, y, width, height }
```

### Trap Tab inside a dialog

GPUIX does not bind Tab. Own the key, then wrap inside the panel with
`focusNextWithin` / `focusPreviousWithin`.

```tsx
function onKeyDown(event: EventPayload) {
  if (event.key !== "tab" || !panel) return;
  if (event.modifiers?.shift) renderer.focusPreviousWithin?.(panel.id);
  else renderer.focusNextWithin?.(panel.id);
}

<div ref={setPanel} onKeyDown={onKeyDown}>
  <div tabIndex={0} autoFocus>
    Ok
  </div>
  <div tabIndex={0}>Cancel</div>
</div>;
```

## Native animations

Use **`motion.div`** to animate from an initial style to a target style. React
sends the target once. Rust calculates intermediate values and requests GPUI
frames until the transition finishes, without a React render or N-API call for
each frame.

### Animate a target

```tsx
import { motion } from "@gpuix/react";

function WelcomeCard() {
  return (
    <motion.div
      initial={{ width: 0, opacity: 0 }}
      animate={{ width: 320, opacity: 1 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      style={{ overflow: "hidden" }}
    >
      <text style={{ color: "#ffffff" }}>Welcome</text>
    </motion.div>
  );
}
```

Set **`initial={false}`** when the element must mount at its first `animate`
target. Later `animate` changes still transition normally. If a target changes
while motion is active, the next transition starts from the current visible
value, so reversing an animation does not jump.

### Targets and timing

Motion currently accepts these **numeric targets**:

| Target                           | Range or unit           |
| -------------------------------- | ----------------------- |
| `width`, `height`                | pixels, zero or greater |
| `top`, `right`, `bottom`, `left` | pixels                  |
| `opacity`                        | `0` through `1`         |
| `borderRadius`                   | pixels, zero or greater |

The **transition** uses seconds, like Motion for React:

| Option     |     Default | Values                                                                              |
| ---------- | ----------: | ----------------------------------------------------------------------------------- |
| `duration` |       `0.3` | Non-negative seconds                                                                |
| `delay`    |         `0` | Non-negative seconds                                                                |
| `ease`     | `"easeOut"` | `"linear"`, `"ease"`, `"easeIn"`, `"easeOut"`, `"easeInOut"`, or `[x1, y1, x2, y2]` |

Springs, keyframes, variants, and shared layout animations are not available
yet. **Exit** uses `AnimatePresence`, like Motion for React.

### Animate a sidebar

Animate an **outer clipping container** and keep the inner sidebar at a fixed
width. This reveals or hides the content without reflowing its text on every
frame.

```tsx
import { motion } from "@gpuix/react";
import type { ReactNode } from "react";

function SidebarFrame({
  collapsed,
  children,
}: {
  collapsed: boolean;
  children: ReactNode;
}) {
  const sidebarWidth = 252;
  const dividerWidth = 1;

  return (
    <motion.div
      initial={false}
      animate={{ width: collapsed ? 0 : sidebarWidth + dividerWidth }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      style={{
        display: "flex",
        flexDirection: "row",
        height: "100%",
        flexShrink: 0,
        overflow: "hidden",
      }}
    >
      <div style={{ width: sidebarWidth, height: "100%", flexShrink: 0 }}>
        {children}
      </div>
      <div style={{ width: dividerWidth, height: "100%", flexShrink: 0 }} />
    </motion.div>
  );
}
```

The **chat example** uses this pattern. The sidebar remains mounted while its
outer width moves between `253` and `0` pixels.

### Animate unmount

A `motion.div` with **`exit`** only leaves after that target finishes, and only
when it is a child of **`AnimatePresence`**. Without `AnimatePresence`, React
destroys the node on the same commit.

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
          transition={{ duration: 0.2, ease: "easeOut" }}
        >
          <text>Saved</text>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
```

Give every child a **unique `key`** when more than one child can leave. Set
**`initial={false}`** on `AnimatePresence` to skip enter on the first paint.
A child with no `exit` is removed without a tween. Exit still completes when
the target already matches, when the node is outside a virtual list's painted
window, or when invalid runtime data makes the native target unusable.

`AnimatePresence` also accepts **`onExitComplete`**, which runs after every
leaving child is gone. `useIsPresent()` reports whether a custom descendant is
leaving. `usePresence()` returns the same status plus `safeToRemove`, for a
custom exit that decides when the retained child can unmount.

```tsx
import { usePresence } from "@gpuix/react";

function DeferredRemoval() {
  const [isPresent, safeToRemove] = usePresence();

  return (
    <div onClick={() => !isPresent && safeToRemove?.()}>
      <text>{isPresent ? "Ready" : "Click to remove"}</text>
    </div>
  );
}
```

`motion.div` accepts **`onMotionComplete`**. It runs when the current native
target settles. If React changes the target before an older completion reaches
JavaScript, the stale completion is ignored.

### Capture exact frames

The [automation API](#automation) can freeze the native motion clock and render
specific timestamps. This avoids timer sleeps and gives CI the same frames on
every run.

```tsx
import { connectTest } from "@gpuix/react/automation";
import { createTestRoot } from "@gpuix/react/testing";
import { ChatApp } from "./chat";

const { render, renderer } = createTestRoot();
render(<ChatApp />);
const app = await connectTest(renderer);

const startedAt = await app.clock.pause();
await app.getByTestId("sidebar-collapse").click();

await app.captureFrames("review/sidebar", [
  startedAt,
  startedAt + 50,
  startedAt + 100,
  startedAt + 150,
  startedAt + 200,
]);

await app.clock.resume();
```
