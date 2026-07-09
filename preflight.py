import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(
    PROJECT_ROOT
    / ".env"
)


def check(condition, success, failure):

    if condition:

        print(
            f"[PASS] {success}"
        )

        return True

    print(
        f"[FAIL] {failure}"
    )

    return False


def main():

    print()
    print("PIPELINE PREFLIGHT CHECK")
    print("-" * 50)

    checks = []

    checks.append(

        check(

            bool(
                os.getenv(
                    "COMPOSIO_API_KEY"
                )
            ),

            "COMPOSIO_API_KEY found",

            "COMPOSIO_API_KEY missing"

        )

    )

    apps_file = (
        PROJECT_ROOT
        / "data"
        / "app.csv"
    )

    checks.append(

        check(

            apps_file.exists(),

            "apps.csv found",

            "apps.csv missing"

        )

    )

    if apps_file.exists():

        dataframe = pd.read_csv(
            apps_file
        )

        checks.append(

            check(

                len(dataframe) == 100,

                "Exactly 100 apps found",

                (
                    f"Expected 100 apps, "
                    f"found {len(dataframe)}"
                )

            )

        )

        checks.append(

            check(

                dataframe["id"].nunique()
                == 100,

                "All app IDs are unique",

                "Duplicate app IDs found"

            )

        )

        checks.append(

            check(

                dataframe["name"].nunique()
                == 100,

                "All app names are unique",

                "Duplicate app names found"

            )

        )

    required_files = [

        "agent/researcher.py",

        "agent/discovery.py",

        "agent/verifier.py",

        "agent/retry.py",

        "agent/final_verifier.py",

        "agent/schemas.py",

        "agent/prompts.py",

        "analysis/accuracy.py",

        "analysis/analyze.py",

        "analysis/create_human_sample.py"

    ]

    for file_name in required_files:

        file_path = (
            PROJECT_ROOT
            / file_name
        )

        checks.append(

            check(

                file_path.exists(),

                f"{file_name} found",

                f"{file_name} missing"

            )

        )

    print()
    print("-" * 50)

    if all(checks):

        print(
            "PREFLIGHT PASSED"
        )

        print(
            "Pipeline is ready to run."
        )

        sys.exit(0)

    print(
        "PREFLIGHT FAILED"
    )

    print(
        "Fix the failed checks before running."
    )

    sys.exit(1)


if __name__ == "__main__":
    main()