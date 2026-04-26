from typing import Iterable


def normalize_requirements(raw_lines: Iterable[str]) -> list[str]:
    cleaned = [line.strip() for line in raw_lines if line.strip()]
    return sorted(set(cleaned))

