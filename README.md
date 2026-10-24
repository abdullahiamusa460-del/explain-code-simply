# explain-code-simply

An Agent Skill that helps an AI agent explain code to a beginner.

## What it does

This skill teaches an AI agent to explain code in plain language, starting with
what the code does and how data moves. The agent maps the file first, follows a
simple six-part structure, and uses real line numbers instead of guessing.

## Example prompts

- "Explain this code to me. I'm new."
- "What does this function do?"
- "Help me understand this file."
- "Explain `src/totals.py` like I'm 12."
- "Walk me through this Python file line by line."

## What is in this repo

- `SKILL.md` — the instruction card the agent always reads.
- `README.md` — this plain-language guide.
- `LICENSE` — the MIT license.
- `.gitignore` — tells Git which local files to ignore.
- `scripts/` — small programs the agent can run to do exact jobs.
  - `scripts/code_map.py` — reads one code file and prints its language, size,
    imports, classes and functions with line numbers, notes, and long lines.
- `references/` — extra reading the agent opens only when needed.
  - `references/explaining-to-beginners.md` — the six-part explanation
    structure, tone rules, good and bad examples, a worked example, and a small
    glossary.

The helper script needs Python 3. Check it with `python3 --version`.

## Install with npx

```bash
npx skills add abdullahiamusa460-del/explain-code-simply
```

## Check it before installing

This lists what the skill contains without installing it:

```bash
npx skills add abdullahiamusa460-del/explain-code-simply --list
```

## Manual install for Claude Code

Clone the repo:

```bash
git clone https://github.com/abdullahiamusa460-del/explain-code-simply.git ~/explain-code-simply
```

Install it for one project:

```bash
mkdir -p .claude/skills
cp -r ~/explain-code-simply .claude/skills/explain-code-simply
```

Install it for yourself, in every project:

```bash
mkdir -p ~/.claude/skills
cp -r ~/explain-code-simply ~/.claude/skills/explain-code-simply
```

## Other agents

Cursor, OpenCode, and other agents are supported through the npx command. The
command detects the agent you use, or asks you to choose one.

## How to test that it works

1. Install the skill.
2. Open a code file in a project.
3. Ask the agent: `Explain this code to me. I'm new.`
4. The skill is working if the agent maps the file first and explains it with
   real line numbers and plain words.

## Hacktoberfest

Built for the Hacktoberfest hackathon. Contributions are welcome. Open an issue
or send a pull request. Good first contributions include clearer examples, more
language support in `scripts/code_map.py`, and fixes to the guide.
