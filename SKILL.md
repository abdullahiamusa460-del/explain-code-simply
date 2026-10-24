---
name: explain-code-simply
description: >-
  Explains code to beginners in plain language, covering what it does, how data
  moves, and why each part exists. Use when someone says "explain this code",
  "what does this function do", "help me understand this file", "explain it
  like I am new", or asks for a beginner-friendly walkthrough.
---

# Explain Code Simply

Help a beginner understand code without changing it. The goal is not a shorter
description. The goal is a reader who can say what the code does, how data moves,
and where to make a change.

## Workflow

1. **Find the code.** Get a file path or a pasted snippet. If neither is clear,
   ask one short question: "Can you paste the code or give me the file path?"
2. **Map a file before explaining it.** Find the folder that contains this
   `SKILL.md` (for a personal Claude Code install, it is
   `~/.claude/skills/explain-code-simply`). Run:

   ```bash
   python3 <skill-folder>/scripts/code_map.py <path-to-file>
   ```

   Use the full path to the user's file if needed. Add `--json` if you need
   structured data. Use the output for exact line numbers, definitions, imports,
   and notes. If the user pasted a snippet, or the script cannot run, skip this
   step and work from the snippet.
3. **Read the style guide.** Read `references/explaining-to-beginners.md`
   before writing the explanation. It has the required six-part structure, tone
   rules, and a worked example.
4. **Write the explanation** in the six parts from the guide: one-sentence
   summary, inputs and outputs, step-by-step walkthrough, words decoded, one
   optional analogy, and a next step.
5. **Check accuracy.** Every line number must exist in the file. Do not invent
   behavior. If you are unsure what a library call does, say so and explain the
   part you can verify.
6. **Stay read-only.** Do not edit, format, or run the user's code unless they
   ask. The map script only reads the file.

## Rules

- Use short sentences and everyday words.
- Define a term the first time you use it.
- Use real names from the code instead of "it" or "this thing".
- Do not say "simply", "just", or "obviously".
- Show a small code excerpt only when it helps. Keep the original line numbers.
- If the file is longer than about 150 lines or has more than 8 definitions,
  explain the map first and ask which part to go through. Do not dump a
  line-by-line walkthrough of a large file.
- If the user asks for a different depth ("like I'm 12", "for an interview"),
  keep the same structure and change the level of detail.

## Examples

**Example 1: a file on disk**

User: "Explain `src/totals.py` to me. I'm new to Python."

Agent:
1. Runs `python3 <skill-folder>/scripts/code_map.py src/totals.py`.
2. Reads `references/explaining-to-beginners.md`.
3. Explains the main function first, then its helper, using the line numbers
   from the map.

**Example 2: a pasted snippet**

User: "What does this do?" (pastes 12 lines of JavaScript)

Agent:
1. Skips the script because there is no file.
2. Reads `references/explaining-to-beginners.md`.
3. Gives the six-part explanation and ends with one small change the user can
   try.
