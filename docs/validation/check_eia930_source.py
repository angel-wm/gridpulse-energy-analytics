"""Validate six public EIA-930 Balance snapshots and export an ERCO batch."""

import argparse
import csv
import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path


FIELDS = (
    "Balancing Authority", "Data Date", "Hour Number", "UTC Time at End of Hour",
    "Demand (MW)", "Demand Forecast (MW)", "Net Generation (MW)",
)
EXPECTED = {
    "2023": (8760, 0, 0, 0, 8760),
    "2024": (8784, 0, 0, 0, 8784),
    "2025": (8760, 48, 48, 48, 8688),
}
PILOT_MONTH = "2025-03"
SOURCE_SHA256 = {
    "EIA930_BALANCE_2023_Jan_Jun.csv": "a0e14e9c07ab4cc1de3e384c7be890b0c61d9de3fe04ad3ae5ec739f1f35ec1b",
    "EIA930_BALANCE_2023_Jul_Dec.csv": "c719fc1b513eec8982ce209b6e3173fc64b2d0d243f83d3bf0d8d1adf6222de2",
    "EIA930_BALANCE_2024_Jan_Jun.csv": "26768c495c3ba987e29d79df2e40d4e741f9dbcff086f53c12ff774465756a10",
    "EIA930_BALANCE_2024_Jul_Dec.csv": "a602a8e577cfdd2fa3083413eaa4dd8ba7f0d2b26a2986f8f6d22917465ea49f",
    "EIA930_BALANCE_2025_Jan_Jun.csv": "fac4bb991dfa1dab3b4b35300ccab54ac99be13a40ce91954db8ddafb2816242",
    "EIA930_BALANCE_2025_Jul_Dec.csv": "1146158b972439db7c7f4cc7d0491e07644ddbf244d03b8ecb44cb2c833d10f1",
}
EXPORT_SCHEMA = (
    ("balancing_authority", "STRING", "REQUIRED"),
    ("reporting_date", "DATE", "REQUIRED"),
    ("reporting_hour_number", "INTEGER", "REQUIRED"),
    ("hour_ending_utc", "TIMESTAMP", "REQUIRED"),
    ("demand_mw", "INTEGER", "NULLABLE"),
    ("forecast_mw", "INTEGER", "NULLABLE"),
    ("net_generation_mw", "INTEGER", "NULLABLE"),
    ("source_file", "STRING", "REQUIRED"),
)


def summarize(rows):
    timestamps = sorted(row[0] for row in rows)
    observed = [row[1] for row in rows if row[1] is not None]
    errors = [
        forecast - demand
        for _, demand, forecast, _ in rows
        if demand is not None and forecast is not None
    ]
    return {
        "hours": len(rows),
        "first_utc": timestamps[0].isoformat(),
        "last_utc": timestamps[-1].isoformat(),
        "duplicates": len(timestamps) - len(set(timestamps)),
        "non_hourly_steps": sum(
            end - start != timedelta(hours=1)
            for start, end in zip(timestamps, timestamps[1:])
        ),
        "missing_demand": len(rows) - len(observed),
        "missing_forecast": sum(row[2] is None for row in rows),
        "missing_generation": sum(row[3] is None for row in rows),
        "paired_hours": len(errors),
        "peak_demand_mw": str(max(observed)) if observed else None,
        "mae_mw": str(round(sum(map(abs, errors)) / len(errors), 6)) if errors else None,
        "bias_mw": str(round(sum(errors) / len(errors), 6)) if errors else None,
    }


def write_projection(output_dir, rows, filename, label):
    output_dir.mkdir()
    csv_path = output_dir / filename
    schema_path = output_dir / "eia930-erco-schema.json"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(name for name, _, _ in EXPORT_SCHEMA)
        writer.writerows(sorted(rows, key=lambda row: row[3]))
    schema = [{"name": name, "type": field_type, "mode": mode}
              for name, field_type, mode in EXPORT_SCHEMA]
    schema_path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    print(label, len(rows), csv_path.stat().st_size, digest, csv_path)


def check_hourly_model(rows):
    """Verify the proposed null and aggregation rules with local SQL."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute(
            "CREATE TABLE raw (hour_ending TEXT PRIMARY KEY, demand INTEGER, forecast INTEGER)"
        )
        connection.executemany(
            "INSERT INTO raw VALUES (?, ?, ?)",
            (
                (hour.isoformat(), None if demand is None else int(demand),
                 None if forecast is None else int(forecast))
                for hour, demand, forecast, _ in rows
            ),
        )
        result = connection.execute("""
            WITH hourly AS (
                SELECT demand, forecast,
                       CASE WHEN demand IS NOT NULL AND forecast IS NOT NULL
                            THEN 1 ELSE 0 END AS paired_hour,
                       forecast - demand AS signed_error,
                       ABS(forecast - demand) AS absolute_error
                FROM raw
            )
            SELECT COUNT(*), SUM(paired_hour), MAX(demand),
                   COUNT(*) FILTER (WHERE demand IS NULL AND forecast IS NOT NULL),
                   COUNT(*) FILTER (WHERE forecast IS NULL AND demand IS NOT NULL),
                   COUNT(*) FILTER (WHERE demand IS NULL AND forecast IS NULL),
                   COUNT(*) FILTER (WHERE paired_hour = 0 AND
                       (signed_error IS NOT NULL OR absolute_error IS NOT NULL)),
                   ROUND(1.0 * SUM(absolute_error) / NULLIF(SUM(paired_hour), 0), 6),
                   ROUND(1.0 * SUM(signed_error) / NULLIF(SUM(paired_hour), 0), 6)
            FROM hourly
        """).fetchone()
        empty_pair_metrics = connection.execute("""
            SELECT AVG(forecast - demand), AVG(ABS(forecast - demand))
            FROM raw
            WHERE demand IS NULL OR forecast IS NULL
        """).fetchone()
    print("hourly model SQL", result, "empty pair selection", empty_pair_metrics)
    return (
        result == (26304, 26232, 85544, 24, 24, 24, 0, 1268.017726, 374.605558)
        and empty_pair_metrics == (None, None)
    )


def check_sources(files, pilot_output, history_output=None):
    all_rows = []
    years = defaultdict(list)
    days = Counter()
    month_rows = []
    export_rows = []
    keys_by_day = defaultdict(list)
    measure_types = Counter()
    file_periods = Counter()
    for path in files:
        with path.open("rb") as source:
            checksum = hashlib.file_digest(source, "sha256").hexdigest()
        if history_output is not None and checksum != SOURCE_SHA256.get(path.name):
            raise ValueError(f"Source snapshot differs from the pinned hash: {path.name}")
        count = 0
        periods = set()
        with path.open(encoding="utf-8-sig", newline="") as source:
            reader = csv.reader(source)
            header = next(reader)
            indexes = [header.index(field) for field in FIELDS]
            for raw in reader:
                if raw[indexes[0]] != "ERCO":
                    continue
                _, date, hour, utc, *values = (raw[index] for index in indexes)
                report_date = datetime.strptime(date, "%m/%d/%Y").date()
                day = report_date.isoformat()
                periods.add((report_date.year, 1 if report_date.month <= 6 else 2))
                days[day] += 1
                keys_by_day[day].append(int(hour))
                timestamp = datetime.strptime(utc, "%m/%d/%Y %I:%M:%S %p")
                measures = [Decimal(value) if value else None for value in values]
                if any(value is not None and not value.is_finite() for value in measures):
                    raise ValueError(f"Nonfinite measurement at {path.name} / {utc}")
                for value in measures:
                    if value is not None:
                        measure_types["fractional" if value % 1 else "integral"] += 1
                row = (timestamp, *measures)
                all_rows.append(row)
                years[day[:4]].append(row)
                if day.startswith(PILOT_MONTH):
                    month_rows.append(row)
                if history_output is not None or (pilot_output is not None and day.startswith(PILOT_MONTH)):
                    half = "Jan_Jun" if report_date.month <= 6 else "Jul_Dec"
                    export_rows.append((
                        "ERCO", day, int(hour), f"{timestamp:%Y-%m-%d %H:%M:%S}+00:00",
                        *(int(value) if value is not None else None for value in measures),
                        f"EIA930_BALANCE_{report_date.year}_{half}.csv",
                    ))
                count += 1
        print(path.name, sorted(periods), path.stat().st_size, checksum, count, sep="\t")
        if len(periods) != 1:
            raise ValueError(f"Expected one reporting half-year in {path.name}")
        file_periods.update(periods)
    expected_fields = (
        "hours", "missing_demand", "missing_forecast", "missing_generation", "paired_hours",
    )
    valid = file_periods == Counter((year, half) for year in range(2023, 2026) for half in (1, 2))
    for year, rows in sorted(years.items()):
        profile = summarize(rows)
        print(year, json.dumps(profile))
        valid &= tuple(profile[key] for key in expected_fields) == EXPECTED.get(year)
    total = summarize(all_rows)
    pilot = summarize(month_rows)
    print("all", json.dumps(total))
    print("pilot", PILOT_MONTH, json.dumps(pilot))
    print("days outside 24 hours", {day: n for day, n in sorted(days.items()) if n != 24})
    hour_exceptions = [
        day for day, keys in sorted(keys_by_day.items()) if sorted(keys) != list(range(1, len(keys) + 1))
    ]
    print("reporting hour exceptions", hour_exceptions)
    print("measure types", dict(measure_types))
    valid = (
        valid
        and total["duplicates"] == 0
        and total["non_hourly_steps"] == 0
        and pilot["hours"] == pilot["paired_hours"] == 743
        and days["2025-03-09"] == 23
        and not hour_exceptions
        and not measure_types["fractional"]
        and check_hourly_model(all_rows)
    )
    if valid and pilot_output is not None:
        write_projection(pilot_output, export_rows, "erco-2025-03.csv", "pilot CSV")
    if valid and history_output is not None:
        write_projection(history_output, export_rows, "erco-2023-2025.csv", "historical CSV")
    return valid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=Path, nargs=6, metavar="CSV")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--pilot-output", type=Path, help="New local folder for the pilot CSV and schema")
    output.add_argument("--history-output", type=Path, help="New local folder for the historical CSV and schema")
    args = parser.parse_args()
    raise SystemExit(0 if check_sources(args.files, args.pilot_output, args.history_output) else 1)
