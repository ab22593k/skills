# Chapter 1 — What Users Do

## Core concepts

- Users form mental models from surface behavior; the interface is the implementation
- Goals, tasks, and actions form a hierarchy: users decompose goals into tasks, tasks into actions
- Working memory holds 7±2 items; recognition beats recall
- Fitts's Law: larger targets closer to cursor are faster to hit
- Norman's gulfs: execution (can user figure out how?) and evaluation (does user understand what happened?)
- Decision-making is biased — users satisfice (choose "good enough"), are influenced by defaults and framing

## Frameworks introduced

- **Gulfs of execution and evaluation** — Debug tool: identify where the interface fails to bridge user intent
- **Seven stages of action (Norman)** — Form goal → plan → specify action → execute → perceive state → interpret → evaluate
- **Fitts's Law** — Mathematical model: MT = a + b log₂(2D/W). Practical: buttons at screen edges are "infinite"
- **Postel's Law** — Be liberal in input acceptance, conservative in output
- **Recognition vs. recall** — Recognition presents options; recall requires memory. Prefer recognition.

## Key techniques

- **Task analysis**: List user goals, decompose into tasks, identify where users fail
- **Affordance mapping**: Every element should look like what it does (button = pressable, slider = draggable)
- **Progressive disclosure**: Hide advanced options behind "Show more" to simplify the primary path
- **Default selection**: Smart defaults reduce cognitive load and guide behavior

## Connection to other chapters

This chapter grounds all subsequent pattern chapters in human behavior. Ch3 (navigation) and Ch4 (layout) derive directly from Fitts's Law and scanning behavior. Ch7 (forms) applies Postel's Law and Miller's Law. Ch9 (visual style) implements recognition over recall.
