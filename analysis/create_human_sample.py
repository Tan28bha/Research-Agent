import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent


FINAL_RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "final_results.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "human_verification_sample.csv"
)


def main():

    with open(
        FINAL_RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        results = json.load(file)

    dataframe = pd.DataFrame(results)

    samples = []

    for category, group in dataframe.groupby(
        "category"
    ):

        sample_size = min(
            2,
            len(group)
        )

        category_sample = group.sample(
            n=sample_size,
            random_state=42
        )

        samples.append(
            category_sample
        )

    sample_dataframe = pd.concat(
        samples
    )

    verification_dataframe = pd.DataFrame({

        "app_id":
            sample_dataframe["id"],

        "app_name":
            sample_dataframe["app_name"],

        "category":
            sample_dataframe["category"],

        "agent_auth":
            sample_dataframe[
                "auth_methods"
            ].apply(
                lambda value:
                ", ".join(value)
            ),

        "agent_access_model":
            sample_dataframe[
                "access_model"
            ],

        "agent_api_types":
            sample_dataframe[
                "api_types"
            ].apply(
                lambda value:
                ", ".join(value)
            ),

        "agent_mcp":
            sample_dataframe[
                "existing_mcp"
            ],

        "agent_buildability":
            sample_dataframe[
                "buildability"
            ],

        "auth_correct": "",

        "access_correct": "",

        "api_correct": "",

        "mcp_correct": "",

        "buildability_correct": "",

        "evidence_correct": "",

        "human_notes": ""
    })

    verification_dataframe.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Human verification sample created."
    )

    print(
        f"Apps sampled: "
        f"{len(verification_dataframe)}"
    )

    print(
        f"Saved to: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()