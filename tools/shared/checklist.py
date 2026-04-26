from typing import Iterable


def render_checklist(items: Iterable[str]) -> str:
    lines = [f"- [ ] {item}" for item in items]
    return "\n".join(lines)

