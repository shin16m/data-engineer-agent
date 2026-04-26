# Agent Tool Matrix

各エージェントが利用可能な Python 補助機能を定義します。

| Agent | Allowed Python Modules |
|---|---|
| `orchestrator-agent` | `tools.shared.io_utils`, `tools.shared.checklist`, `tools.agent_tool_registry` |
| `requirements-agent` | `tools.shared.io_utils`, `tools.requirements_tools`, `tools.agent_tool_registry` |
| `design-agent` | `tools.shared.io_utils`, `tools.design_tools`, `tools.agent_tool_registry` |
| `implementation-agent` | `tools.shared.io_utils`, `tools.implementation_tools`, `tools.agent_tool_registry` |
| `qa-agent` | `tools.shared.io_utils`, `tools.shared.checklist`, `tools.qa_tools`, `tools.agent_tool_registry` |

## Source of Truth

最終的な参照元は `tools/agent_tool_registry.py` です。
このファイルと差分が出た場合は、registry 側を優先します。

