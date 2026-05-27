# Running Rust from Web Browsers

## Core concepts

- **WebAssembly (Wasm)** is a binary instruction format that runs in browsers at near-native speed
- **`wasm-pack`** builds, tests, and publishes Rust-generated Wasm packages for JavaScript consumption
- **`wasm-bindgen`** enables Rust functions to be called from JavaScript and vice versa
- **`cargo-generate`** scaffolds new projects from templates (e.g., `wasm-pack-template`)
- Output: `.wasm` binary, `.js` glue code, `package.json`, `.d.ts` type declarations

## Frameworks introduced

**Rust-to-Wasm pipeline** — 1) Write Rust with `#[wasm_bindgen]` annotations. 2) `wasm-pack build` compiles to Wasm + JS glue. 3) npm project imports the generated package. 4) JavaScript calls Rust functions as if they were native JS.

## Key techniques

- `#[wasm_bindgen]` on functions exports them to JavaScript
- Call JS from Rust: `#[wasm_bindgen] extern "C" { fn alert(s: &str); }`
- Full-stack auth example: Rust `login(uname, passwd) -> bool` called from JS `loginButton.onclick = () => { const result = wasm.login(uname, pwd); }`
- Build: `wasm-pack build`
- Dev server: `npm init wasm-app www` → `npm run start`

## Code examples

```rust
use wasm_bindgen::prelude::*;

// Call JavaScript from Rust
#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
}

// Export Rust function to JavaScript
#[wasm_bindgen]
pub fn greet(name: &str) {
    alert(&format!("Hello, {}!", name));
}

// Login authentication — called from JS
#[wasm_bindgen]
pub fn login(uname: &str, passwd: &str) -> bool {
    uname == "abhishek" && passwd == "rust"
}
```

## Connection to other chapters

WASM uses `extern "C"` FFI patterns (Ch17) for JavaScript interop. The build pipeline extends cargo (Ch1). `wasm-bindgen` is itself a macro/proc-macro crate building on generics (Ch7).
