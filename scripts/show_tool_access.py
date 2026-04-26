from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.agent_tool_registry import registry


def main() -> int:
    print("# Agent Tool Access")
    for agent, tools in registry().items():
        print(f"\n[{agent}]")
        for tool in tools:
            print(f"- {tool}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

