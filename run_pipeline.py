import subprocess
import sys
import time
from pathlib import Path


PIPELINE_STEPS = [

    (
        "FIRST-PASS RESEARCH",
        [
            sys.executable,
            "agent/researcher.py"
        ]
    ),

    (
        "RAW RESULT VALIDATION",
        [
            sys.executable,
            "agent/validate_raw.py"
        ]
    ),

    (
        "FIRST VERIFICATION",
        [
            sys.executable,
            "agent/verifier.py"
        ]
    ),

    (
        "TARGETED RETRY",
        [
            sys.executable,
            "agent/retry.py"
        ]
    ),

    (
        "FINAL VERIFICATION",
        [
            sys.executable,
            "agent/final_verifier.py"
        ]
    ),

    (
        "CONFIDENCE ANALYSIS",
        [
            sys.executable,
            "analysis/accuracy.py"
        ]
    ),

    (
        "PATTERN ANALYSIS",
        [
            sys.executable,
            "analysis/analyze.py"
        ]
    ),

    (
        "HUMAN SAMPLE GENERATION",
        [
            sys.executable,
            "analysis/create_human_sample.py"
        ]
    )
]


def run_step(name, command):

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    start_time = time.time()

    result = subprocess.run(
        command
    )

    duration = (
        time.time()
        - start_time
    )

    if result.returncode != 0:

        print()
        print(
            f"{name} FAILED."
        )

        print(
            "Pipeline stopped."
        )

        sys.exit(
            result.returncode
        )

    print()

    print(
        f"{name} COMPLETED "
        f"in {duration:.2f} seconds."
    )


def main():

    pipeline_start = time.time()

    print()
    print("=" * 60)
    print("API LANDSCAPE RESEARCH PIPELINE")
    print("=" * 60)

    for name, command in PIPELINE_STEPS:

        run_step(
            name,
            command
        )

    print()
    print("=" * 60)
    print("SYNCING DATA TO WEB DIRECTORY")
    print("=" * 60)
    try:
        import shutil
        shutil.copy2(PROJECT_ROOT / "data" / "final_results.json", PROJECT_ROOT / "web" / "data" / "final_results.json")
        shutil.copy2(PROJECT_ROOT / "data" / "analysis_summary.json", PROJECT_ROOT / "web" / "data" / "analysis_summary.json")
        shutil.copy2(PROJECT_ROOT / "data" / "accuracy_summary.json", PROJECT_ROOT / "web" / "data" / "accuracy_summary.json")
        print("Data successfully synced to web/data/")
    except Exception as e:
        print(f"Failed to sync data to web/data/: {e}")

    total_duration = (
        time.time()
        - pipeline_start
    )

    print()
    print("=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    print(
        f"Total runtime: "
        f"{total_duration / 60:.2f} minutes"
    )


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent
    main()