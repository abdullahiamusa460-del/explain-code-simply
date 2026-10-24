#!/usr/bin/env python3
"""Map one source file so an agent can explain it to a beginner.

What it does:
    Reads one source file and prints a quick map: language, size, imports,
    classes and functions with exact line numbers, TODO notes, and very long
    lines. It never changes the file and uses only the Python standard library.

How to run:
    python3 scripts/code_map.py path/to/file.py
    python3 scripts/code_map.py path/to/file.py --json

The line numbers are exact. The comment and code counts are approximate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LANGUAGES = {
    ".py": "Python",
    ".pyw": "Python",
    ".js": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".jsx": "JavaScript (React)",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React)",
    ".java": "Java",
    ".c": "C",
    ".h": "C or C++ header",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++ header",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".sh": "Bash",
    ".bash": "Bash",
    ".zsh": "Zsh",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sql": "SQL",
    ".json": "JSON",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
    ".md": "Markdown",
}

HASH_COMMENT = {"Python", "Ruby", "Bash", "Zsh", "YAML", "TOML"}

SLASH_COMMENT = {
    "JavaScript",
    "JavaScript (React)",
    "TypeScript",
    "TypeScript (React)",
    "Java",
    "C",
    "C or C++ header",
    "C++",
    "C++ header",
    "C#",
    "Go",
    "Rust",
    "Kotlin",
    "Swift",
    "PHP",
}

KEYWORDS = {
    "if",
    "for",
    "while",
    "switch",
    "catch",
    "return",
    "else",
    "do",
    "try",
    "function",
    "class",
    "new",
    "delete",
    "throw",
    "case",
    "sizeof",
    "typeof",
    "await",
    "yield",
    "with",
}

IMPORT_RE = re.compile(
    r"^\s*(?:import\b|from\s+[\w.]+\s+import\b|use\b|#include\b|"
    r"require\s*\(|const\s+[A-Za-z_$][\w$]*\s*=\s*require\s*\(|"
    r"source\b|using\s+[A-Za-z_])"
)

GENERIC_PATTERNS = [
    (
        "class",
        re.compile(
            r"^(?:export\s+)?(?:default\s+)?(?:public\s+|private\s+|"
            r"protected\s+|abstract\s+|final\s+|sealed\s+|static\s+|"
            r"open\s+)*class\s+([A-Za-z_$][\w$]*)"
        ),
    ),
    (
        "type",
        re.compile(
            r"^(?:export\s+)?(?:public\s+)?(?:interface|struct|enum|trait)"
            r"\s+([A-Za-z_$][\w$]*)"
        ),
    ),
    (
        "type",
        re.compile(r"^type\s+([A-Za-z_]\w*)\s+(?:struct|interface)\b"),
    ),
    (
        "type",
        re.compile(r"^(?:export\s+)?type\s+([A-Za-z_$][\w$]*)\s*(?:=|$)"),
    ),
    (
        "function",
        re.compile(
            r"^(?:export\s+)?(?:default\s+)?(?:public\s+|private\s+|"
            r"protected\s+|static\s+|async\s+|extern\s+|inline\s+)*"
            r"function\s+([A-Za-z_$][\w$]*)"
        ),
    ),
    (
        "function",
        re.compile(
            r"^(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)"
            r"\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)"
            r"\s*=>"
        ),
    ),
    (
        "function",
        re.compile(r"^func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)"),
    ),
    (
        "function",
        re.compile(
            r"^(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?(?:unsafe\s+)?"
            r"fn\s+([A-Za-z_]\w*)"
        ),
    ),
    (
        "function",
        re.compile(r"^def\s+(?:self\.)?([A-Za-z_]\w*[?!=]?)"),
    ),
    (
        "class",
        re.compile(r"^(?:class|module)\s+([A-Za-z_]\w*)"),
    ),
    (
        "function",
        re.compile(
            r"^(?:(?:public|private|protected|static|final|abstract|"
            r"synchronized|native|default|async|override|virtual|inline|"
            r"constexpr|extern|open|suspend|operator)\s+)*"
            r"fun(?:c)?\s+([A-Za-z_]\w*)"
        ),
    ),
    (
        "function",
        re.compile(
            r"^(?:(?:public|private|protected|static|final|abstract|"
            r"synchronized|native|default|async|override|virtual|inline|"
            r"constexpr|extern)\s+)+[\w:<>\[\],*&?]+\s+"
            r"([A-Za-z_]\w*)\s*\([^;{}]*\)\s*(?:const\s*)?(?:\{|$)"
        ),
    ),
    (
        "function",
        re.compile(
            r"^(?:const\s+)?[\w:<>\[\],*&?]+\s+([A-Za-z_]\w*)"
            r"\s*\([^;{}]*\)\s*(?:const\s*)?\{"
        ),
    ),
    (
        "function",
        re.compile(
            r"^(?:static\s+)?(?:async\s+)?(?:get\s+|set\s+)?"
            r"([A-Za-z_$][\w$]*)\s*\([^;{}]*\)\s*\{"
        ),
    ),
    (
        "function",
        re.compile(r"^(?:function\s+)?([A-Za-z_]\w*)\s*\(\)\s*\{"),
    ),
    (
        "table",
        re.compile(
            r"^CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW|FUNCTION|"
            r"PROCEDURE)\s+([A-Za-z_][\w.]*)",
            re.IGNORECASE,
        ),
    ),
]


def detect_language(path: Path, first_line: str) -> str:
    """Guess the language from the file extension, then from a shebang."""
    language = LANGUAGES.get(path.suffix.lower())
    if language:
        return language

    if first_line.startswith("#!"):
        lowered = first_line.lower()
        if "python" in lowered:
            return "Python"
        if "bash" in lowered:
            return "Bash"
        if "zsh" in lowered:
            return "Zsh"
        if "ruby" in lowered:
            return "Ruby"
        if "node" in lowered:
            return "JavaScript"

    return "Unknown"


def is_comment_only(line: str, language: str) -> bool:
    """Return True when a line looks like a comment and nothing else."""
    stripped = line.strip()
    if not stripped:
        return False

    if language in HASH_COMMENT:
        return stripped.startswith("#")

    if language in SLASH_COMMENT:
        return stripped.startswith(("//", "/*", "*"))

    if language in {"CSS", "SCSS"}:
        return stripped.startswith(("/*", "*"))

    if language == "HTML":
        return stripped.startswith("<!--")

    if language == "SQL":
        return stripped.startswith("--")

    if language == "PHP":
        return stripped.startswith(("//", "#", "/*", "*"))

    return False


def python_definitions(lines: list[str]) -> list[dict]:
    """Find Python classes and functions, keeping their indentation depth."""
    found = []
    for number, raw in enumerate(lines, start=1):
        stripped = raw.lstrip()
        indent = len(raw) - len(stripped)

        match = re.match(r"^(?:async\s+)?def\s+([A-Za-z_]\w*)\s*\(", stripped)
        if match:
            found.append(
                {
                    "line": number,
                    "kind": "function",
                    "name": match.group(1),
                    "depth": indent // 4,
                }
            )
            continue

        match = re.match(r"^class\s+([A-Za-z_]\w*)", stripped)
        if match:
            found.append(
                {
                    "line": number,
                    "kind": "class",
                    "name": match.group(1),
                    "depth": indent // 4,
                }
            )

    return found


def generic_definitions(lines: list[str]) -> list[dict]:
    """Find classes, types, and functions in common brace-based languages."""
    found = []
    for number, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped:
            continue

        for kind, pattern in GENERIC_PATTERNS:
            match = pattern.match(stripped)
            if not match:
                continue
            name = match.group(1)
            if name in KEYWORDS:
                break
            found.append(
                {"line": number, "kind": kind, "name": name, "depth": 0}
            )
            break

    return found


def collect(path: Path, text: str) -> dict:
    """Build the map data for one file."""
    lines = text.splitlines()
    first_line = lines[0] if lines else ""
    language = detect_language(path, first_line)

    blank = sum(1 for line in lines if not line.strip())
    comments = sum(1 for line in lines if is_comment_only(line, language))
    code = len(lines) - blank - comments

    imports = []
    for number, line in enumerate(lines, start=1):
        if IMPORT_RE.match(line):
            imports.append({"line": number, "text": line.strip()[:120]})

    definitions = (
        python_definitions(lines) if language == "Python" else generic_definitions(lines)
    )

    long_lines = [
        {"line": number, "length": len(line)}
        for number, line in enumerate(lines, start=1)
        if len(line) > 100
    ]

    notes = []
    for number, line in enumerate(lines, start=1):
        if re.search(
            r"(?:#|//|/\*|<!--|--)\s*(?:TODO|FIXME|HACK|XXX)\b",
            line,
            re.IGNORECASE,
        ):
            notes.append({"line": number, "text": line.strip()[:120]})

    start_line = definitions[0]["line"] if definitions else 1
    return {
        "file": str(path),
        "language": language,
        "line_counts": {
            "total": len(lines),
            "code": code,
            "comment_only": comments,
            "blank": blank,
        },
        "start_line": start_line,
        "long_lines": long_lines,
        "imports": imports,
        "definitions": definitions,
        "notes": notes,
    }


def print_text(data: dict) -> None:
    """Print the map in a form that is easy to read in a chat."""
    counts = data["line_counts"]
    print(f"File: {data['file']}")
    print(f"Language: {data['language']}")
    print(
        f"Lines: {counts['total']} total "
        f"({counts['code']} code, {counts['comment_only']} comment-only, "
        f"{counts['blank']} blank)"
    )

    definitions = data["definitions"]
    if definitions:
        first = definitions[0]
        print(f"Start here: line {first['line']} ({first['kind']} {first['name']})")
    else:
        print("Start here: line 1 (top of file)")

    long_lines = data["long_lines"]
    if long_lines:
        shown = ", ".join(
            f"line {item['line']} ({item['length']} chars)"
            for item in long_lines[:5]
        )
        extra = len(long_lines) - 5
        suffix = f" and {extra} more" if extra > 0 else ""
        print(f"Long lines over 100 characters: {len(long_lines)} -> {shown}{suffix}")
    else:
        print("Long lines over 100 characters: none")

    imports = data["imports"]
    if imports:
        print(f"Imports: {len(imports)}")
        for item in imports[:12]:
            print(f"  line {item['line']}: {item['text']}")
        if len(imports) > 12:
            print(f"  ... and {len(imports) - 12} more")
    else:
        print("Imports: none")

    if definitions:
        print(f"Definitions: {len(definitions)}")
        for item in definitions[:40]:
            pad = "  " * min(item["depth"], 4)
            print(
                f"  line {item['line']}: {pad}{item['kind']} {item['name']}"
            )
        if len(definitions) > 40:
            print(f"  ... and {len(definitions) - 40} more")
    else:
        print("Definitions: none (this may be a config, data, or style file)")

    notes = data["notes"]
    if notes:
        print(f"Notes: {len(notes)}")
        for item in notes[:10]:
            print(f"  line {item['line']}: {item['text']}")
        if len(notes) > 10:
            print(f"  ... and {len(notes) - 10} more")
    else:
        print("Notes: none")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Map one source file for a beginner-friendly explanation."
    )
    parser.add_argument("file", help="path to one source file")
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the map as JSON instead of text",
    )
    args = parser.parse_args()

    path = Path(args.file).expanduser()

    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1
    if path.is_dir():
        print(f"Error: {path} is a folder. Point me at one file.", file=sys.stderr)
        return 1

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        print(f"Error: could not read {path}: {error}", file=sys.stderr)
        return 1

    data = collect(path, text)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_text(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
