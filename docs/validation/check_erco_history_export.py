"""Reconcile the curated Power BI CSV with the approved ERCO snapshot."""

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path


FIELDS = (
    "balancing_authority", "reporting_date", "reporting_hour_number", "hour_ending_utc",
    "demand_mw", "forecast_mw", "net_generation_mw", "source_file", "local_start_hour",
    "paired_hour", "forecast_error_mw", "absolute_error_mw",
)
EXPECTED_CLOCK_DAYS = {
    "2023-03-12": 23, "2023-11-05": 25, "2024-03-10": 23,
    "2024-11-03": 25, "2025-03-09": 23, "2025-11-02": 25,
}


def read_integer(value):
    return None if value == "" else int(value)


def check_export(path):
    dates = Counter()
    years = Counter()
    missing = Counter()
    signed_errors = []
    demand_values = []
    previous_utc = None
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream)
        if tuple(rows.fieldnames or ()) != FIELDS:
            raise ValueError("Unexpected CSV columns or order")
        for number, row in enumerate(rows, start=2):
            if None in row or None in row.values() or row["balancing_authority"] != "ERCO":
                raise ValueError(f"Unexpected row shape or authority at line {number}")
            timestamp = datetime.strptime(row["hour_ending_utc"], "%Y-%m-%dT%H:%M:%SZ")
            expected_utc = datetime(2023, 1, 1, 7) if previous_utc is None else previous_utc + timedelta(hours=1)
            if timestamp != expected_utc:
                raise ValueError(f"Missing, duplicated, or unordered UTC hour at line {number}")
            previous_utc = timestamp
            reporting_date = date.fromisoformat(row["reporting_date"])
            dates[row["reporting_date"]] += 1
            years[reporting_date.year] += 1
            half = "Jan_Jun" if reporting_date.month <= 6 else "Jul_Dec"
            if row["source_file"] != f"EIA930_BALANCE_{reporting_date.year}_{half}.csv":
                raise ValueError(f"Unexpected source filename at line {number}")
            if int(row["reporting_hour_number"]) != dates[row["reporting_date"]] or not 0 <= int(row["local_start_hour"]) <= 23:
                raise ValueError(f"Unexpected reporting or local hour at line {number}")
            demand = read_integer(row["demand_mw"])
            forecast = read_integer(row["forecast_mw"])
            paired = demand is not None and forecast is not None
            signed = forecast - demand if paired else None
            absolute = abs(signed) if signed is not None else None
            if (int(row["paired_hour"]), read_integer(row["forecast_error_mw"]),
                    read_integer(row["absolute_error_mw"])) != (int(paired), signed, absolute):
                raise ValueError(f"Forecast fields disagree with the inputs at line {number}")
            if paired:
                signed_errors.append(signed)
            else:
                missing[(demand is None, forecast is None)] += 1
            if demand is not None:
                demand_values.append(demand)
            if read_integer(row["net_generation_mw"]) is None:
                missing["generation"] += 1

    clock_days = {day: hours for day, hours in dates.items() if hours != 24}
    if (years != {2023: 8760, 2024: 8784, 2025: 8760} or len(dates) != 1096
            or min(dates) != "2023-01-01" or max(dates) != "2025-12-31"
            or previous_utc != datetime(2026, 1, 1, 6) or clock_days != EXPECTED_CLOCK_DAYS):
        raise ValueError("Historical date or UTC coverage differs from the baseline")
    if missing != {(True, False): 24, (False, True): 24, (True, True): 24, "generation": 48}:
        raise ValueError("Missing-measure counts differ from the baseline")

    pairs = len(signed_errors)
    if pairs != 26232:
        raise ValueError("Paired-hour count differs from the baseline")
    peak = max(demand_values)
    mae = round(Decimal(sum(map(abs, signed_errors))) / pairs, 6)
    bias = round(Decimal(sum(signed_errors)) / pairs, 6)
    if (peak, mae, bias) != (85544, Decimal("1268.017726"), Decimal("374.605558")):
        raise ValueError("Historical KPIs differ from the baseline")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {
        "hours": sum(years.values()), "utc_keys": sum(years.values()),
        "paired_hours": pairs, "reporting_dates": len(dates), "years": dict(years),
        "peak_mw": peak, "mae_mw": str(mae), "bias_mw": str(bias),
        "csv_bytes": path.stat().st_size, "sha256": digest,
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("csv", type=Path)
    print(json.dumps(check_export(cli.parse_args().csv)))
