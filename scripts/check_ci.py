"""Run the static CI checks without contacting a data warehouse."""

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("pilot", "history", "recovery")


def main():
    static = subprocess.run([sys.executable, "scripts/check_local.py"], cwd=ROOT)
    if static.returncode:
        return static.returncode
    dbt_env = {
        name: value
        for name, value in os.environ.items()
        if name.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "TMPDIR"}
    }
    dbt_env.update(
        GRIDPULSE_PROJECT_ID="gridpulse-offline",
        DBT_SEND_ANONYMOUS_USAGE_STATS="false",
        DBT_PARTIAL_PARSE="false",
    )
    for target in TARGETS:
        print(f"Parse dbt target: {target}", flush=True)
        parsed = subprocess.run(
            [
                sys.executable,
                "-c",
                "from dbt.cli.main import cli; cli()",
                "parse",
                "--project-dir", "dbt",
                "--profiles-dir", "dbt",
                "--target", target,
            ],
            cwd=ROOT,
            env=dbt_env,
        )
        if parsed.returncode:
            return parsed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
