# Multi-Agent Project Template

orchestration を中心に、複数エージェントが協調して開発を進めるためのプロジェクト雛形です。

## Principles

- エージェントの振る舞いは `SKILL.md` で定義する
- 補助機能は Python スクリプトとして実装する
- 各エージェントが利用できる補助機能を明確に管理する

## Directory Layout

- `.cursor/skills/` : エージェント別スキル定義
- `tools/` : エージェントが使う補助機能 (Python)
- `scripts/` : 運用スクリプト
- `docs/agent-tool-matrix.md` : エージェントとツールの対応表

## Agent Roles

- `orchestrator-agent` : タスク分解、担当割り当て、進行管理
- `requirements-agent` : 要件定義・受け入れ条件の明確化
- `design-agent` : 設計案作成・トレードオフ整理
- `implementation-agent` : 実装手順化・変更計画作成
- `qa-agent` : テスト観点と品質ゲート策定

## Tool Access Policy

単一のレジストリ `tools/agent_tool_registry.py` で、各エージェントの利用可能ツールを管理します。
これにより「誰が何を実行できるか」をコード上で明示できます。

## Quick Start

```bash
python scripts/validate_project.py
python scripts/show_tool_access.py
```

# AI Agent Project (Skill-Driven)

AIエージェント開発を、`SKILL.md` を中心に進めるためのプロジェクト雛形です。  
Cursorが自動で参照しやすいよう、プロジェクトスキルを `.cursor/skills/` に配置しています。
モデル実行は Cursor AI を利用し、Pythonは補助ツール（検証・評価）として使います。

## スキル構成

- `.cursor/skills/ai-agent-planner/SKILL.md`
  - 要件整理、制約抽出、マイルストーン設計
- `.cursor/skills/ai-agent-implementer/SKILL.md`
  - 実装時の分割方針、品質チェック、実装ガードレール
- `.cursor/skills/ai-agent-evaluator/SKILL.md`
  - 評価観点、失敗分析、回帰テスト運用

## 使い方

1. まず要件定義時に `ai-agent-planner` を使う
2. 実装フェーズで `ai-agent-implementer` を使う
3. 検証・改善フェーズで `ai-agent-evaluator` を使う

### Pythonツール連携（推奨）

`SKILL.md` は手順と判断基準、`scripts/*.py` は再現可能な処理を担当します。

```bash
python scripts/validate_env.py
python scripts/eval_agent.py --cases data/test_cases.json --outputs data/agent_outputs.json
```

- `scripts/validate_env.py` : 必須ファイル構成の検証
- `scripts/eval_agent.py` : テストケースと出力JSONの照合評価
- `data/test_cases.json` : 評価ケースのサンプル
- `data/agent_outputs.json` : Cursor AIの出力サンプル

## 補足

このテンプレートは OpenAI API キー不要で動作します。  
Cursor AIの応答を `data/agent_outputs.json` に保存して評価に使ってください。
