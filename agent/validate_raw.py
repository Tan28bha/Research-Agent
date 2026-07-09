import json
import sys
from pathlib import Path
from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "agent"))

from schemas import AppResearchResult

def main():
    raw_file = PROJECT_ROOT / "data" / "raw_results.json"
    if not raw_file.exists():
        print("Raw results file does not exist.")
        sys.exit(1)
        
    try:
        with open(raw_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load raw results: {e}")
        sys.exit(1)
        
    print(f"Validating {len(data)} raw results...")
    errors = 0
    for idx, item in enumerate(data):
        try:
            AppResearchResult(**item)
        except ValidationError as e:
            print(f"Validation failed for item {idx} (ID: {item.get('id')}): {e}")
            errors += 1
            
    if errors > 0:
        print(f"Validation failed with {errors} errors.")
        sys.exit(1)
        
    print("All raw results validated successfully.")

if __name__ == "__main__":
    main()
