import json
import sys
from pathlib import Path

from tqdm import tqdm


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(Path(__file__).resolve().parent))

from verifier import verify_app


FINAL_RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "final_results.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "final_verifications.json"
)


def load_json(file_path):

    if not file_path.exists():
        return []

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_json(file_path, data):

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def main():

    final_results = load_json(
        FINAL_RESULTS_FILE
    )

    existing_verifications = load_json(
        OUTPUT_FILE
    )

    completed_ids = {
        result["app_id"]
        for result in existing_verifications
    }

    results = existing_verifications.copy()

    pending_results = [
        result
        for result in final_results
        if result["id"] not in completed_ids
    ]

    print(
        f"Final results: "
        f"{len(final_results)}"
    )

    print(
        f"Already verified: "
        f"{len(completed_ids)}"
    )

    print(
        f"Remaining: "
        f"{len(pending_results)}"
    )

    import threading
    from concurrent.futures import ThreadPoolExecutor, as_completed

    save_lock = threading.Lock()

    def process_final_verification(app_result):
        try:
            verification = verify_app(app_result)
            with save_lock:
                results.append(verification.model_dump(mode="json"))
                save_json(OUTPUT_FILE, results)
        except Exception as error:
            print(f"\nFailed final verification for {app_result['app_name']}: {error}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_final_verification, app_result) for app_result in pending_results]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Final verification"):
            pass

    print()

    print(
        f"Final verification complete. "
        f"{len(results)} results saved."
    )


if __name__ == "__main__":
    main()