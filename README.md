# データ前処理エージェント

データ分析前の事前処理に特化した単一エージェント構成です。  
異なるファイル形式・フォーマットのソースデータを解釈し、正規化されたテーブルデータへ変換します。

## 構成

```text
.cursor/
  rules/
    persona-data-normalization.mdc
  skills/
    data-normalization-agent/SKILL.md
  config/
    normalization_defaults.yaml
```

## エージェントの役割

- `data-normalization-agent`
  - 入力データの形式判定とスキーマ解釈
  - 列名・型・単位の標準化
  - フラット化または正規化テーブル分割
  - 品質チェックと変換結果レポート生成

## 基本ワークフロー

1. `input` と `output` だけ受け取る
2. `.cursor/config/normalization_defaults.yaml` の固定ルールを読み込む
3. 入力データを正規化テーブルへ変換
4. 固定の品質ゲートで検証
5. 変換結果・スキーマ・品質レポートを出力

## 最小リクエスト

```text
データ事前処理をお願いします。
input: data/raw/
output: data/processed/
```

## ペルソナ + スキル構成

- ペルソナは `.cursor/rules/persona-data-normalization.mdc` で常時適用されます。
- 実処理は `.cursor/skills/data-normalization-agent/SKILL.md` を利用します。
- 役割分離:
  - ペルソナ: 品質優先・出力形式・ガードレールを定義
  - スキル: 正規化の具体的な実行手順を定義

### リクエスト例

```text
データ事前処理をお願いします。
input: data/raw/
output: data/processed/
```

期待される返却:
- 処理サマリー
- 出力スキーマ
- 品質チェック結果（pass/fail）
- 未解決課題と次アクション

## 補足

- 変換ルールと品質チェックは `.cursor/config/normalization_defaults.yaml` で固定管理します。
- 例外対応が必要なときだけ、`overrides` を追加して差分指定します。
- 実行スクリプトは常設せず、処理依頼時にエージェントが都度生成します。
