import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "final_results.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "analysis_summary.json"
)


def load_results():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def percentage(
    value,
    total
):

    if total == 0:
        return 0

    return round(
        (
            value
            / total
        )
        * 100,
        2
    )


def main():

    results = load_results()

    total_apps = len(results)

    auth_counter = Counter()

    access_counter = Counter()

    buildability_counter = Counter()

    blocker_counter = Counter()

    api_breadth_counter = Counter()

    category_counter = Counter()

    mcp_count = 0

    for app in results:

        for auth_method in app.get(
            "auth_methods",
            []
        ):

            auth_counter[
                auth_method
            ] += 1

        access_counter[
            app.get(
                "access_model",
                "unknown"
            )
        ] += 1

        buildability_counter[
            app.get(
                "buildability",
                "unknown"
            )
        ] += 1

        blocker_counter[
            app.get(
                "primary_blocker",
                "unknown"
            )
        ] += 1

        api_breadth_counter[
            app.get(
                "api_breadth",
                "unknown"
            )
        ] += 1

        category_counter[
            app.get(
                "category",
                "unknown"
            )
        ] += 1

        if app.get(
            "existing_mcp",
            False
        ):

            mcp_count += 1

    high_buildability = (
        buildability_counter.get(
            "high",
            0
        )
    )

    self_serve = (
        access_counter.get(
            "self_serve_free",
            0
        )
        +
        access_counter.get(
            "self_serve_trial",
            0
        )
    )

    summary = {

        "total_apps":
            total_apps,

        "headline_metrics": {

            "high_buildability_count":
                high_buildability,

            "high_buildability_percentage":
                percentage(
                    high_buildability,
                    total_apps
                ),

            "self_serve_count":
                self_serve,

            "self_serve_percentage":
                percentage(
                    self_serve,
                    total_apps
                ),

            "existing_mcp_count":
                mcp_count,

            "existing_mcp_percentage":
                percentage(
                    mcp_count,
                    total_apps
                )
        },

        "auth_distribution":
            dict(
                auth_counter.most_common()
            ),

        "access_distribution":
            dict(
                access_counter.most_common()
            ),

        "buildability_distribution":
            dict(
                buildability_counter.most_common()
            ),

        "blocker_distribution":
            dict(
                blocker_counter.most_common()
            ),

        "api_breadth_distribution":
            dict(
                api_breadth_counter.most_common()
            ),

        "category_distribution":
            dict(
                category_counter.most_common()
            )
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
    print("ANALYSIS COMPLETE")
    print("-----------------------------")

    print(
        f"Total Apps: "
        f"{total_apps}"
    )

    print(
        f"Highly Buildable: "
        f"{high_buildability}"
    )

    print(
        f"Self Serve: "
        f"{self_serve}"
    )

    print(
        f"Existing MCPs: "
        f"{mcp_count}"
    )

    print()

    print("Top Authentication Methods")

    for method, count in auth_counter.most_common():

        print(
            f"{method}: {count}"
        )

    print()

    print("Top Blockers")

    for blocker, count in blocker_counter.most_common(
        10
    ):

        print(
            f"{blocker}: {count}"
        )

    print("-----------------------------")


if __name__ == "__main__":
    main()