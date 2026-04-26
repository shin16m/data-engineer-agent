from collections.abc import Mapping


AGENT_TOOL_ACCESS: dict[str, list[str]] = {
    "orchestrator-agent": [
        "tools.shared.io_utils",
        "tools.shared.checklist",
        "tools.agent_tool_registry",
    ],
    "requirements-agent": [
        "tools.shared.io_utils",
        "tools.requirements_tools",
        "tools.agent_tool_registry",
    ],
    "design-agent": [
        "tools.shared.io_utils",
        "tools.design_tools",
        "tools.agent_tool_registry",
    ],
    "implementation-agent": [
        "tools.shared.io_utils",
        "tools.implementation_tools",
        "tools.agent_tool_registry",
    ],
    "qa-agent": [
        "tools.shared.io_utils",
        "tools.shared.checklist",
        "tools.qa_tools",
        "tools.agent_tool_registry",
    ],
}


def allowed_tools(agent_name: str) -> list[str]:
    return AGENT_TOOL_ACCESS.get(agent_name, [])


def is_tool_allowed(agent_name: str, tool_module: str) -> bool:
    return tool_module in AGENT_TOOL_ACCESS.get(agent_name, [])


def registry() -> Mapping[str, list[str]]:
    return AGENT_TOOL_ACCESS

