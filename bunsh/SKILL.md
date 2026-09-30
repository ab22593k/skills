---
name: bunsh
description: Reference for Bun — its runtime, package manager, test runner, and bundler. Use whenever the user mentions Bun, bunfig.toml, bun.lock, bunx, "bun install", "bun test", "bun build", "bun --watch"/"--hot", "bun run", Bun APIs (Bun.file, Bun.serve, bun:sqlite), or moving a project from npm/pnpm to Bun. Also use for Bun-specific friction even when the user doesn't name Bun — a test file that never runs, a postinstall that silently didn't fire, an env var that comes back undefined in a bundle, or picking between --watch and --hot. Consult this before guessing at Bun CLI flags or bunfig.toml keys, because Bun silently accepts config it does not recognize rather than erroring.
---

# Bun Reference

Bun is a single binary that replaces Node.js, npm, the test runner, and the
bundler. This is a reference card — reach for it when the task touches Bun
specifically, not as general JavaScript guidance.

Companion skills: `release-it` (readiness review), `vercel-react-best-practices`
(React perf), `web-design-guidelines` (UI review). Bun's own docs at
<https://bun.com/docs> remain the source of truth; this card is the fast path.

## Reach for Bun when

- Running `.ts`/`.jsx`/`.tsx` files with no build step (`bun run script.ts`)
- Installing dependencies — the same `bun install` works in any Node project
- Running Jest-style tests, in parallel, with no config file
- Building browser or server bundles (`bun build`)
- Dev loops that need restart-on-change (`--watch`) or state-preserving reload
  (`--hot`)
- Monorepos, where `bun install --filter` and workspace protocols are first-class

## Do not reach for Bun for

- **Type checking.** Bun transpiles, it does not type-check. Run `tsc --noEmit`
  (or your framework's checker) separately and wire it into CI. Bun's bundler
  will happily emit code that does not compile.
- **Generating `.d.ts` declarations** — same reason; use `tsc --emitDeclarationOnly`.
- **Node-only APIs Bun hasn't implemented.** Before depending on an edge of the
  Node compatibility surface, check <https://bun.com/docs/runtime/nodejs-apis>.
  The gap list is real and it moves; don't assume.

## Command reference

| Task                      | Command                                        |
| ------------------------- | ---------------------------------------------- |
| Run a file                | `bun run script.ts` (or just `bun script.ts`)  |
| Run a package.json script | `bun run dev`                                  |
| Install deps              | `bun install` / `bun i`                        |
| Add a package             | `bun add react` · dev: `bun add -d typescript` |
| Remove a package          | `bun remove react`                             |
| Run tests                 | `bun test`                                     |
| Coverage                  | `bun test --coverage`                          |
| Bundle                    | `bun build ./index.ts --outdir ./dist`         |
| Restart on change         | `bun --watch run script.ts`                    |
| Hot reload                | `bun --hot run server.ts`                      |
| Run a package binary      | `bunx cowsay "hi"` (`-i` to install it first)  |
| Print resolved env        | `bun --print process.env`                      |
| One-off eval              | `bun -e 'console.log(Bun.version)'`            |

### Flags belong after `bun`, not after the subcommand

```sh
bun --watch run dev      # ✅ watcher wraps the script
bun run dev --watch      # ❌ --watch is passed through to the script itself
```

This trips people up constantly because it inverts the convention from npm.
Trailing args are forwarded to the target, which is occasionally what you want
(`bun run test -- --reporter=jest`) but is never what you want for Bun's own flags.

### `bun run <name>` resolves scripts before files

If `package.json` has a `dev` script _and_ a `dev.ts` file exists, `bun run dev`
runs the script. Force the file with an explicit path: `bun run ./dev.ts`.

`bun run` is also the only way to reach shell builtins and system binaries —
`bun run ls` works, bare `bun ls` does not.

## Configuration files

| File            | Purpose                                                   |
| --------------- | --------------------------------------------------------- |
| `bunfig.toml`   | Bun-specific settings (test, install, runtime)            |
| `package.json`  | Scripts, deps, workspaces, `trustedDependencies`          |
| `tsconfig.json` | TypeScript options — Bun reads it, but doesn't enforce it |
| `.env*`         | Auto-loaded env files (see below)                         |
| `bun.lock`      | Text lockfile, committed to VCS                           |

`bun.lock` is the current default and is human-readable. Older `bun.lockb`
(binary) projects convert on the next install; see the lockfile gotcha below.

### bunfig.toml

```toml
[test]
preload = ["./setup.ts"]   # runs before each test file
coverage = true
coverageThreshold = 0.9   # non-zero exit if overall coverage falls below this
pathIgnorePatterns = ["**/e2e/**"]

[install]
linker = "isolated"        # or "hoisted" (default) — see decision table
```

**`bunfig.toml` never errors on keys it doesn't recognize.** A typo is accepted
and ignored in complete silence, so you get a config that looks correct and
does nothing. This is the single most expensive trap in this file: when a
setting "isn't working," verify the setting changes _observable behavior_
(coverage numbers, which test files run) rather than assuming absence of an
error means the key is valid. If you're unsure whether a key exists, check the
docs instead of adding it and watching for a warning that will never come.

Coverage thresholds are enforced through the process exit code, not printed as
a threshold message — `bun test` returning non-zero is your CI signal.

## Decision tables

### `hoisted` vs `isolated`

| Situation                  | Linker     | Why                                                 |
| -------------------------- | ---------- | --------------------------------------------------- |
| New monorepo / workspace   | `isolated` | Prevents phantom deps, strict per-package isolation |
| New single-package project | `hoisted`  | Matches npm's layout, fewer surprises               |
| Existing project           | `hoisted`  | Changing the linker rewrites `node_modules` layout  |
| Migrating from pnpm        | `isolated` | Closest to pnpm's semantics                         |

Set via `bun install --linker isolated` or `[install] linker`. In `hoisted` mode
a package can import a dependency it never declared — the bug surfaces as
"works on my machine" long after the layout change, so prefer `isolated` for
anything with more than one package.

### `--watch` vs `--hot`

| Situation                                 | Use                 | Behavior                               |
| ----------------------------------------- | ------------------- | -------------------------------------- |
| Long-running process, clean state matters | `--watch`           | Full restart                           |
| HTTP server / dev loop                    | `--hot`             | Soft reload, preserves globals, faster |
| Tests                                     | `bun test --watch`  | Re-runs affected files                 |
| Bundling                                  | `bun build --watch` | Incremental rebuild                    |

`--hot` re-executes modules in place. That's the speed win and the hazard:
module-level state (caches, DB pools, in-memory maps) can survive a reload and
quietly go stale. Reach for `--watch` when in doubt.

### `bun run` vs direct execution

| Situation                       | Command          | Why                          |
| ------------------------------- | ---------------- | ---------------------------- |
| package.json script             | `bun run dev`    | Runs pre/post hooks          |
| A file, no script               | `bun script.ts`  | Skips script lookup          |
| Local CLI (`node_modules/.bin`) | `bun run eslint` | Resolves local binaries      |
| System command / builtin        | `bun run ls`     | Only reachable via `bun run` |

## Tests

Discovery is filename-based: `*.test.ts`, `*_test.ts`, `*.spec.ts`, `*_spec.ts`
(and the `.js`/`.jsx`/`.tsx` variants). A file that doesn't match is not
"failing" — it is invisible, and `bun test` will report a green run that
silently skipped it. If someone insists a test never runs, check the filename
before anything else.

```ts
import { test, expect, mock } from "bun:test";

test("adds", () => {
  expect(1 + 1).toBe(2);
});

test("with a mock", () => {
  const spy = mock(() => 42);
  expect(spy()).toBe(42);
});
```

The runner is Jest-compatible, so most existing `describe`/`it`/`beforeEach`
suites and `expect` matchers port without edits. `bun:test` also exports
`mock`, `spyOn`, and `jest.fn`-style helpers.

## Environment variables

Bun loads `.env` automatically — `dotenv` and `dotenv-expand` are unnecessary
dependencies in a Bun project. Files load in increasing precedence:

1. `.env`
2. `.env.production` / `.env.development` / `.env.test` (selected by `NODE_ENV`)
3. `.env.local` (skipped when `NODE_ENV=test`)
4. `.env.<env>.local`

Bun expands `$VAR` references, which makes connection strings readable:

```ini
DB_HOST=localhost
DB_URL=postgres://$DB_USER@$DB_HOST:5432/$DB_NAME
```

Escape a literal `$` with `\$`. `Bun.env` and `import.meta.env` are aliases of
`process.env`.

Override the file set with `--env-file=...` (repeatable, and it accepts a pipe
or `/dev/stdin` for secrets you don't want on disk), or turn automatic loading
off with `--no-env-file` or `env = false` in `bunfig.toml` — worth doing in
containers that should rely only on real process env.

`BUN_OPTIONS` prepends arguments to every Bun invocation in the environment
(`BUN_OPTIONS="--hot"` makes `bun run dev` behave like `bun --hot run dev`),
which is a clean way to set a repo-wide default without editing scripts.

### Keep env access literal

```ts
export const token = process.env.API_TOKEN; // ✅ substitutable
const env = process.env;
export const key = env.API_TOKEN; // ⚠️ misses substitution
```

The mechanism is explicit substitution — chiefly `bun build --define
process.env.API_TOKEN='"..."'`, and any bundler define/inline step. Given a
literal `process.env.X`, the value is inlined; given the destructured alias, the
substitution is **silently skipped** and the bundle keeps a runtime lookup.
A default build inlines neither, so this only bites once you add a define step —
which is exactly why it reaches production. Always access `process.env.X`
directly.

## Gotchas

**`bunfig.toml` silently ignores unknown keys.** Covered above — the highest-value
entry in this list. Verify behavior, not absence of errors.

**Lifecycle scripts are off by default.** Bun does not run `postinstall` for
dependencies unless the package is listed in `trustedDependencies` in
`package.json`:

```json
{ "trustedDependencies": ["esbuild", "sharp"] }
```

Symptom: a package installs fine but its native binary is missing, and nothing
warns you. Trust packages you actually depend on — the list is a security
boundary, so don't reflexively trust everything.

**Auto-install only fires without `node_modules`.** In the default `auto` mode
Bun installs missing packages from its global cache only when no `node_modules`
exists. Once a `node_modules` is present, Bun defers to it and a missing package
is a hard error. That's the correct behavior, but it means "it auto-installed
yesterday, why not today" usually means someone ran `bun init`/`bun install`
in between. Three modes, per `bun --help`:

| Mode             | Behavior                                           |
| ---------------- | -------------------------------------------------- |
| `auto` (default) | Auto-installs when there is no `node_modules`      |
| `fallback`       | Installs only the specific missing packages (`-i`) |
| `force`          | Always installs                                    |

Use `fallback`/`-i` in throwaway scripts and CI one-liners; `auto` in a repo.

**A green test run can mean zero tests ran.** Discovery is filename-based and
a miss is silent. Confirm the file count in the summary line, not just the
color.

**The bundler doesn't type-check.** `bun build` emitting a bundle says nothing
about types. Keep `tsc --noEmit` in CI.

**Env vars must be read literally** — see the section above.

**Lockfile churn from binary lockfiles.** Projects created before Bun v1.2 have
`bun.lockb`. The text `bun.lock` is current; let Bun rewrite it and commit the
result rather than hand-converting.

## Bundling

```sh
bun build ./index.tsx --outdir ./dist --target browser --minify
bun build ./server.ts  --outdir ./dist --target node --format cjs
```

`--target` drives platform assumptions (browser bundles get a DOM, `node`
targets keep Node builtins external). Minify with `--minify`; add
`--sourcemap=linked` or `=external` to ship maps. Plugins register through
Bun's plugin API when a bundler plugin needs to be adapted.

## Monorepos

```sh
bun install                       # install everything
bun install --filter web          # only the `web` workspace
bun run --filter '*' build        # build every workspace
```

Workspace dependencies use the `workspace:*` protocol. `isolated` is the sane
default here — it keeps each package honest about what it imports.

## Verifying a change

- `bun install` completes and `bun.lock` is committed
- `bun test` passes **and the file count matches your expectations**
- `tsc --noEmit` is clean if the project type-checks at all
- `bun build` completes if a bundle is part of the deliverable
- `.env` / secrets are present for the environment you're actually running in
- Any `bunfig.toml` key you added demonstrably changes behavior

## Unverified in this card

Kept honest deliberately: this card's behavioral claims were checked against
**Bun 1.4.2**. A few items are carried from the docs and are _not_ locally
verified — `trustedDependencies`, the `[install]` boolean keys
(`dev`/`optional`/`production`), and TypeScript type-integration specifics
(which have moved as TypeScript has; Bun does not type-check either way). Check
<https://bun.com/docs> before relying on those. Perf claims from marketing copy
are omitted on purpose: they don't change a decision, and they age badly.
