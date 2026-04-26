from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


def parse_date(raw: str) -> Optional[str]:
    text = (raw or "").strip()
    if not text:
        return None
    if "/" in text:
        parts = text.split("/")
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            y, m, d = parts
            try:
                return datetime(int(y), int(m), int(d)).strftime("%Y-%m-%d")
            except ValueError:
                pass
    formats = [
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%Y.%m.%d",
        "%m-%d-%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def parse_number(raw: str) -> Optional[float]:
    text = (raw or "").strip()
    if not text or text in {"?", "-"}:
        return None
    cleaned = text.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_unit(raw: str) -> Optional[str]:
    text = (raw or "").strip()
    if not text:
        return None
    mapping = {"個": "unit_count", "%": "unit_percent", "万円": "unit_ten_thousand_jpy"}
    return mapping.get(text, text.lower().replace(" ", "_"))


def normalize_file(input_file: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    rejects_dir = output_dir / "rejects"
    rejects_dir.mkdir(parents=True, exist_ok=True)

    normalized_path = output_dir / "fact_test.csv"
    rejects_path = rejects_dir / "fact_test_rejects.csv"
    report_path = output_dir / "quality_report.json"
    schema_path = output_dir / "schema.json"
    rules_path = output_dir / "transformation_rules.json"

    total_lines = 0
    source_records = 0
    output_records = 0
    reject_records = 0
    duplicate_records = 0
    null_value_count = 0
    invalid_value_count = 0
    invalid_date_count = 0

    seen_keys = set()
    normalized_rows = []
    reject_rows = []

    with input_file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        data_section = False
        for row in reader:
            total_lines += 1
            if not row:
                continue
            joined = ",".join(row).strip()
            if not joined:
                continue
            if joined.startswith("#"):
                continue
            if not data_section:
                if row[:5] == ["Name", "Value", "Date", "Unit", "Notes"]:
                    data_section = True
                continue

            # Handle rows with too many or too few columns.
            row = (row + ["", "", "", "", ""])[:5]
            name, raw_value, raw_date, raw_unit, notes = [cell.strip() for cell in row]

            if not any([name, raw_value, raw_date, raw_unit, notes]):
                continue

            source_records += 1
            date_iso = parse_date(raw_date)
            value_num = parse_number(raw_value)
            unit_norm = normalize_unit(raw_unit)

            if raw_date and date_iso is None:
                invalid_date_count += 1
            if raw_value and value_num is None:
                invalid_value_count += 1

            record = {
                "name": name or None,
                "value": value_num,
                "date": date_iso,
                "unit": unit_norm,
                "notes": notes or None,
            }

            if record["value"] is None:
                null_value_count += 1

            # Required fields: name, value, date
            if not record["name"] or record["value"] is None or not record["date"]:
                reject_records += 1
                reject_rows.append(
                    {
                        **record,
                        "reject_reason": "missing_required_fields_or_invalid_type",
                        "raw_value": raw_value or None,
                        "raw_date": raw_date or None,
                        "raw_unit": raw_unit or None,
                    }
                )
                continue

            key = (record["name"], record["date"])
            if key in seen_keys:
                duplicate_records += 1
                reject_records += 1
                reject_rows.append(
                    {
                        **record,
                        "reject_reason": "duplicate_primary_key",
                        "raw_value": raw_value or None,
                        "raw_date": raw_date or None,
                        "raw_unit": raw_unit or None,
                    }
                )
                continue

            seen_keys.add(key)
            output_records += 1
            normalized_rows.append(record)

    with normalized_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "value", "date", "unit", "notes"])
        writer.writeheader()
        writer.writerows(normalized_rows)

    with rejects_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "value",
                "date",
                "unit",
                "notes",
                "reject_reason",
                "raw_value",
                "raw_date",
                "raw_unit",
            ],
        )
        writer.writeheader()
        writer.writerows(reject_rows)

    schema = {
        "table": "fact_test",
        "columns": {
            "name": "string",
            "value": "float",
            "date": "date(YYYY-MM-DD)",
            "unit": "string|null",
            "notes": "string|null",
        },
        "primary_key": ["name", "date"],
    }
    schema_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")

    rules = {
        "column_name_case": "snake_case",
        "date_format": "YYYY-MM-DD",
        "number_parsing": "remove_thousands_separator_then_float",
        "unit_mapping": {
            "個": "unit_count",
            "%": "unit_percent",
            "万円": "unit_ten_thousand_jpy",
        },
        "required_fields": ["name", "value", "date"],
        "dedup_key": ["name", "date"],
    }
    rules_path.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")

    report = {
        "input_file": str(input_file),
        "output_table": str(normalized_path),
        "rejects_file": str(rejects_path),
        "total_lines": total_lines,
        "source_records": source_records,
        "output_records": output_records,
        "reject_records": reject_records,
        "duplicate_records": duplicate_records,
        "null_value_count": null_value_count,
        "invalid_value_count": invalid_value_count,
        "invalid_date_count": invalid_date_count,
        "row_count_reconciliation_ok": (source_records == output_records + reject_records),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run default data preprocessing.")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", required=True, help="Output directory path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if input_path.is_dir():
        csv_files = sorted(input_path.glob("*.csv"))
        if not csv_files:
            raise SystemExit(f"No CSV files found in input directory: {input_path}")
        input_path = csv_files[0]
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    report = normalize_file(input_path, output_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
