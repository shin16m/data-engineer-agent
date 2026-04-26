# Data Preprocessing Agent

データ分析前の事前処理に特化した単一エージェント構成です。  
異なるファイル形式・フォーマットのソースデータを解釈し、正規化されたテーブルデータへ変換します。

## Structure

```text
.cursor/
  skills/
    data-normalization-agent/SKILL.md
config/
  normalization_defaults.yaml
```

## Agent Role

- `data-normalization-agent`
  - 入力データの形式判定とスキーマ解釈
  - 列名・型・単位の標準化
  - フラット化または正規化テーブル分割
  - 品質チェックと変換結果レポート生成

## Typical Workflow

1. `input` と `output` だけ受け取る
2. `config/normalization_defaults.yaml` の固定ルールを読み込む
3. 入力データを正規化テーブルへ変換
4. 固定の品質ゲートで検証
5. 変換結果・スキーマ・品質レポートを出力

## Minimal Request

```text
データ事前処理をお願いします。
input: data/raw/
output: data/processed/
```

## Notes

- 変換ルールと品質チェックは `config/normalization_defaults.yaml` で固定管理します。
- 例外対応が必要なときだけ、`overrides` を追加して差分指定します。
