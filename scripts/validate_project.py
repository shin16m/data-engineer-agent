from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.agent_tool_registry import registry


def main() -> int:
    required = [
        Path(".cursor/skills/orchestrator-agent/SKILL.md"),
        Path(".cursor/skills/requirements-agent/SKILL.md"),
        Path(".cursor/skills/design-agent/SKILL.md"),
        Path(".cursor/skills/implementation-agent/SKILL.md"),
        Path(".cursor/skills/qa-agent/SKILL.md"),
        Path("tools/agent_tool_registry.py"),
        Path("docs/agent-tool-matrix.md"),
    ]

    errors: list[str] = []
    for path in required:
        if not path.exists():
            errors.append(f"Missing required file: {path}")

    access = registry()
    if not access:
        errors.append("Agent tool registry is empty.")

    for agent, tools in access.items():
        if not tools:
            errors.append(f"{agent} has no allowed tools.")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

