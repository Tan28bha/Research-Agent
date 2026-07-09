import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


FIRST_VERIFICATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "verified_results.json"
)

FINAL_VERIFICATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "final_verifications.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "accuracy_summary.json"
)


def load_json(file_path):

    if not file_path.exists():
        return []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def average(values):

    if not values:
        return 0

    return sum(values) / len(values)


def main():

    first_results = load_json(
        FIRST_VERIFICATION_FILE
    )

    final_results = load_json(
        FINAL_VERIFICATION_FILE
    )

    first_map = {
        result["app_id"]: result
        for result in first_results
    }

    final_map = {
        result["app_id"]: result
        for result in final_results
    }

    common_ids = (
        set(first_map.keys())
        & set(final_map.keys())
    )

    first_confidences = []

    final_confidences = []

    improved_apps = []

    declined_apps = []

    unchanged_apps = []

    for app_id in common_ids:

        first = first_map[app_id]

        final = final_map[app_id]

        first_score = first[
            "final_confidence_score"
        ]

        final_score = final[
            "final_confidence_score"
        ]

        first_confidences.append(
            first_score
        )

        final_confidences.append(
            final_score
        )

        difference = (
            final_score
            - first_score
        )

        app_summary = {
            "app_id": app_id,
            "app_name": final["app_name"],
            "first_confidence": first_score,
            "final_confidence": final_score,
            "difference": round(
                difference,
                4
            )
        }

        if difference > 0.01:

            improved_apps.append(
                app_summary
            )

        elif difference < -0.01:

            declined_apps.append(
                app_summary
            )

        else:

            unchanged_apps.append(
                app_summary
            )

    first_average = average(
        first_confidences
    )

    final_average = average(
        final_confidences
    )

    summary = {

        "total_compared": len(
            common_ids
        ),

        "first_pass_average_confidence": round(
            first_average,
            4
        ),

        "final_average_confidence": round(
            final_average,
            4
        ),

        "confidence_change": round(
            final_average
            - first_average,
            4
        ),

        "improved_count": len(
            improved_apps
        ),

        "declined_count": len(
            declined_apps
        ),

        "unchanged_count": len(
            unchanged_apps
        ),

        "improved_apps": improved_apps,

        "declined_apps": declined_apps,

        "unchanged_apps": unchanged_apps
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("ACCURACY SUMMARY")
    print("-----------------------------")

    print(
        f"Apps compared: "
        f"{len(common_ids)}"
    )

    print(
        f"First-pass confidence: "
        f"{first_average:.2%}"
    )

    print(
        f"Final confidence: "
        f"{final_average:.2%}"
    )

    print(
        f"Confidence change: "
        f"{final_average - first_average:+.2%}"
    )

    print(
        f"Improved apps: "
        f"{len(improved_apps)}"
    )

    print(
        f"Declined apps: "
        f"{len(declined_apps)}"
    )

    print(
        f"Unchanged apps: "
        f"{len(unchanged_apps)}"
    )

    print("-----------------------------")


if __name__ == "__main__":
    main()