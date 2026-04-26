# AI Agent Project Template

`orchestrator` を中心に複数エージェントが連携する、最小構成のテンプレートです。  
各エージェントの振る舞いは `SKILL.md` に集約します。

## Minimal Structure

```text
.cursor/
  skills/
    orchestrator-agent/SKILL.md
    requirements-agent/SKILL.md
    design-agent/SKILL.md
    implementation-agent/SKILL.md
    qa-agent/SKILL.md
```

## Agent Roles

- `orchestrator-agent`
  - 依頼を分解し、各エージェントへタスクを割り当てる中心役
- `requirements-agent`
  - 要件整理、スコープ定義、受け入れ条件の明確化
- `design-agent`
  - 設計オプション作成、トレードオフ比較、推奨案提示
- `implementation-agent`
  - ファイル単位の実装手順と検証手順を作成
- `qa-agent`
  - リスクベースのテスト計画と品質ゲートを定義

## Typical Workflow

1. `orchestrator-agent` が依頼を4フェーズに分解する
2. `requirements-agent` が受け入れ条件を作る
3. `design-agent` が実装方針を決める
4. `implementation-agent` が変更計画を作る
5. `qa-agent` が品質ゲートを定義する
6. `orchestrator-agent` が最終統合して完了判定する

## Notes

- 最小構成のため、まずは `SKILL.md` のみで運用可能です。
- 必要になったら `scripts/` や `tools/` を後から追加してください。
