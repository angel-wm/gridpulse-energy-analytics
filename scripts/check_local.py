"""Check maintained documentation links and Python syntax without cloud access."""

import ast
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
LINK = re.compile(r"\[[^\]]+\]\(([^\s)]+)\)")


def anchors(document):
    seen = Counter()
    result = set()
    for title in HEADING.findall(document):
        slug = re.sub(r"[^\w -]", "", title.lower()).replace(" ", "-")
        count = seen[slug]
        seen[slug] += 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def main():
    documents = sorted([*ROOT.glob("*.md"), *(ROOT / "docs").rglob("*.md")])
    errors = []
    count = 0
    for source in documents:
        content = source.read_text(encoding="utf-8")
        for link in LINK.findall(content):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            count += 1
            target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            if not target.exists():
                errors.append(f"{source.relative_to(ROOT)}: missing target {link}")
            elif parsed.fragment and target.suffix.lower() == ".md":
                if unquote(parsed.fragment) not in anchors(target.read_text(encoding="utf-8")):
                    errors.append(f"{source.relative_to(ROOT)}: missing heading {link}")

    python_files = sorted([
        *(ROOT / "scripts").rglob("*.py"),
        *(ROOT / "docs" / "validation").rglob("*.py"),
    ])
    for path in python_files:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path.relative_to(ROOT)))
        except SyntaxError as error:
            errors.append(f"{error.filename}:{error.lineno}: {error.msg}")

    for error in errors:
        print(error)
    print(f"Checked {count} documentation links and {len(python_files)} Python files.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
