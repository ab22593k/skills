---
name: opencode-agents
description: >-
  Configure, create, and manage OpenCode agents — primary agents and subagents with custom prompts, models, tool permissions, and modes.
  Use this skill whenever the user asks about OpenCode agents, configuring agents, creating custom agents,
  agent permissions, switching agents, agent modes (primary/subagent/all), the @ mention system, built-in agents
  (Build, Plan, General, Explore, Scout), the `opencode agent create` command, agent options (description,
  temperature, max steps, steps, disable, prompt, model, permissions, mode, hidden, color, top_p), agent configuration
  in JSON or Markdown, or task permissions for subagent invocation. Also use when the user needs help setting up
  a code reviewer agent, documentation agent, security auditor agent, or any other custom agent workflow.
---

# OpenCode Agents

OpenCode agents are specialized AI assistants with custom prompts, models, and tool access. There are two types:
**primary agents** (main conversation, cycled with **Tab** or `switch_agent` keybind) and **subagents** (invoked via
`@mention` or automatically by primary agents via the Task tool).

## Built-in Agents

### Primary agents

| Agent | Description |
|---|---|
| **Build** | Default primary agent. All tools enabled. Full development access. |
| **Plan** | Restricted read-only agent. `edit: ask`, `bash: ask`. Analysis without changes. |
| **Compaction** | Hidden system agent — compacts long context. Runs automatically. |
| **Title** | Hidden system agent — generates session titles. Runs automatically. |
| **Summary** | Hidden system agent — creates session summaries. Runs automatically. |

### Subagents

| Agent | Description |
|---|---|
| **General** | Full tool access (except todo). Complex multi-step research and tasks. |
| **Explore** | Fast, read-only. Codebase exploration — patterns, keywords, questions. |
| **Scout** | Read-only. External docs and dependency research — clone repos, inspect library source. |

## Configuration

Agents are configured in `opencode.json` (global `~/.config/opencode/opencode.json` or per-project `opencode.json`)
or as standalone Markdown files (`~/.config/opencode/agents/<name>.md` or `.opencode/agents/<name>.md`).

### JSON syntax

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "my-agent": {
      "description": "What this agent does and when to use it",
      "mode": "subagent",    // "primary" | "subagent" | "all"
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "You are a specialized assistant. Focus on X.",
      "temperature": 0.1,
      "steps": 10,           // max agentic iterations (replaces deprecated maxSteps)
      "permission": {
        "edit": "deny",
        "bash": "deny"
      },
      "hidden": false,       // hide from @ autocomplete
      "color": "#ff6b6b",    // hex or theme color
      "topP": 0.9,
      "disable": false       // disable the agent
    }
  }
}
```

### Markdown syntax

Place `.md` files in `~/.config/opencode/agents/` or `.opencode/agents/`. The filename becomes the agent name.

```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: deny
---

You are in code review mode. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations
```

## Agent Options

### description (required)
Brief description of what the agent does and when it should be used. Primary agents also show this in the agent switcher.

### temperature
Control response randomness: `0.0-0.2` focused/deterministic (analysis, planning), `0.3-0.5` balanced (general dev),
`0.6-1.0` creative (brainstorming). Defaults: 0 for most models, 0.55 for Qwen.

### steps (max iterations)
Max number of agentic iterations before forced text-only response. `maxSteps` is deprecated — use `steps`.

### disable
Set to `true` to disable the agent.

### prompt
Custom system prompt file path relative to config location: `"{file:./prompts/my-agent.txt}"`.

### model
Override the model for this agent. Format: `provider/model-id` (e.g. `anthropic/claude-sonnet-4-20250514`).
Primary agents default to the globally configured model; subagents default to the invoking agent's model.

### permissions
Control tool access per agent. Each key: `"allow"` | `"ask"` | `"deny"`.

Available permission keys:
- **read** — file reads
- **edit** — file modifications (write, edit, apply_patch)
- **glob** — file pattern matching
- **grep** — content search
- **list** — directory listing
- **bash** — shell commands (supports granular glob patterns per command)
- **task** — subagent invocation (supports glob patterns like `"orchestrator-*": "allow"`)
- **external_directory** — file access outside the project worktree
- **todowrite** — task list management
- **webfetch** — URL fetching
- **websearch** — web search
- **lsp** — LSP queries
- **skill** — loading skills
- **question** — asking the user questions
- **doom_loop** — recovery when tool call repeats 3× with same input

Granular bash permissions example:
```jsonc
"permission": {
  "bash": {
    "*": "ask",
    "git push": "ask",
    "grep *": "allow"
  }
}
```
Last matching rule wins — put `"*"` first and specific rules after.

Task permissions control which subagents an agent can invoke:
```jsonc
"permission": {
  "task": {
    "*": "deny",
    "orchestrator-*": "allow",
    "code-reviewer": "ask"
  }
}
```
Users can still invoke any subagent directly via `@`.

### mode
`"primary"` — main conversation agent (cycled via Tab). `"subagent"` — invoked via @mention or Task tool.
`"all"` — both. Defaults to `"all"` if not specified.

### hidden
Only for `mode: subagent`. Hides from `@` autocomplete menu. Can still be invoked via Task tool.

### color
Visual appearance in UI. Hex color (e.g. `#FF5733`) or theme color (`primary`, `secondary`, `accent`, `success`, `warning`, `error`, `info`).

### topP
Alternative to temperature for controlling response diversity. Range 0.0-1.0.

### additional
Any extra options are passed through directly to the provider as model options (e.g. `reasoningEffort`, `textVerbosity`).

```jsonc
{
  "agent": {
    "deep-thinker": {
      "reasoningEffort": "high",
      "textVerbosity": "low"
    }
  }
}
```

## Creating Agents

Use the `opencode agent create` interactive command:
1. Choose global (`~/.config/opencode/agents/`) or project-specific (`.opencode/agents/`)
2. Describe what the agent should do
3. OpenCode generates the system prompt and identifier
4. Select which permissions to allow (unselected = denied)
5. A Markdown agent file is created

## Usage

- **Tab** or `switch_agent` keybind — cycle primary agents
- **@mention** subagents in messages: `@general help me search for this function`
- **Session navigation**: `session_child_first` (default `<Leader>+Down`) to enter child sessions, `session_child_cycle` (**Right**) / `session_child_cycle_reverse` (**Left**) to navigate, `session_parent` (**Up**) to return

## Agent Design Patterns

| Pattern | Mode | Permissions | Use case |
|---|---|---|---|
| Full stack dev | primary | all tools allowed | General development |
| Planner | primary | edit: ask, bash: ask | Code analysis, architecture design |
| Code reviewer | subagent | edit: deny | Read-only code review |
| Debugger | subagent | read: allow, bash: allow | Bug investigation |
| Security auditor | subagent | edit: deny | Vulnerability scanning |
| Docs writer | subagent | bash: deny | Documentation creation |

## Examples

### Documentation agent (`~/.config/opencode/agents/docs-writer.md`)
```markdown
---
description: Writes and maintains project documentation
mode: subagent
permission:
  bash: deny
---
You are a technical writer. Create clear, comprehensive documentation.
Focus on: clear explanations, proper structure, code examples, user-friendly language.
```

### Security auditor (`~/.config/opencode/agents/security-auditor.md`)
```markdown
---
description: Performs security audits and identifies vulnerabilities
mode: subagent
permission:
  edit: deny
---
You are a security expert. Look for: input validation vulnerabilities,
authentication and authorization flaws, data exposure risks, dependency vulnerabilities.
```

### Orchestrator with task permissions (`opencode.json`)
```jsonc
{
  "agent": {
    "orchestrator": {
      "mode": "primary",
      "permission": {
        "task": {
          "*": "deny",
          "orchestrator-*": "allow",
          "code-reviewer": "ask"
        }
      }
    }
  }
}
```
