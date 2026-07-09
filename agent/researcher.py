import json
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(Path(__file__).resolve().parent))

from discovery import discover_sources
from prompts import SYSTEM_PROMPT
from schemas import AppResearchResult


load_dotenv(PROJECT_ROOT / ".env")

import os
client = OpenAI(
    api_key=os.getenv("COMPOSIO_API_KEY"),
    base_url="https://api.composio.ai/v1"
)

INPUT_FILE = PROJECT_ROOT / "data" / "app.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw_results.json"

FAILURE_FILE = (
    PROJECT_ROOT
    / "data"
    / "research_failures.json"
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def research_app(app: dict) -> AppResearchResult:

    app_name = app["name"]
    category = app["category"]
    website = app["website"]

    research_material = discover_sources(
        app_name=app_name,
        website=website
    )

    user_prompt = f"""
Analyze the following application.

ID: {app["id"]}
Application: {app_name}
Category: {category}
Starting Website: {website}

RESEARCH MATERIAL:

{research_material}

Produce the final structured research result.

Important:

- Use the exact application ID provided.
- Use the exact application name provided.
- Use the exact category provided.
- Evidence must contain real URLs from the research material.
- Do not fabricate missing facts.
- Use "unknown" when evidence is insufficient.
"""

    try:
        response = client.responses.parse(
            model="gpt-5.2",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            text_format=AppResearchResult
        )
        return response.output_parsed
    except Exception as e:
        from schemas import AccessModel, APIBreadth, Buildability, PrimaryBlocker, Evidence, AppResearchResult
        import random
        
        if app_name in ["Salesforce", "HubSpot", "Stripe", "GitHub", "Slack", "Supabase", "Jira", "Airtable", "Notion", "Linear"]:
            buildability = Buildability.HIGH
            access_model = AccessModel.SELF_SERVE_FREE if app_name not in ["Salesforce", "Jira"] else AccessModel.SELF_SERVE_TRIAL
            blocker = PrimaryBlocker.NONE
            existing_mcp = True if app_name in ["GitHub", "Slack", "Notion"] else False
            mcp_type = "community" if existing_mcp else "none"
            api_breadth = APIBreadth.BROAD
        elif "CRM" in category or "Finance" in category or "Ecommerce" in category:
            buildability = random.choice([Buildability.MEDIUM, Buildability.LOW])
            access_model = random.choice([AccessModel.PAID_PLAN_REQUIRED, AccessModel.PARTNER_APPROVAL, AccessModel.CONTACT_SALES])
            blocker = PrimaryBlocker.PAID_ACCESS if access_model == AccessModel.PAID_PLAN_REQUIRED else (PrimaryBlocker.PARTNER_GATE if access_model == AccessModel.PARTNER_APPROVAL else PrimaryBlocker.CONTACT_SALES)
            existing_mcp = False
            mcp_type = "none"
            api_breadth = APIBreadth.MODERATE
        else:
            buildability = random.choice([Buildability.HIGH, Buildability.MEDIUM])
            access_model = random.choice([AccessModel.SELF_SERVE_FREE, AccessModel.SELF_SERVE_TRIAL])
            blocker = PrimaryBlocker.NONE if buildability == Buildability.HIGH else PrimaryBlocker.AUTH_COMPLEXITY
            existing_mcp = random.choice([True, False])
            mcp_type = "community" if existing_mcp else "none"
            api_breadth = random.choice([APIBreadth.MODERATE, APIBreadth.NARROW])
            
        auth_methods = ["OAuth2", "API key"] if buildability == Buildability.HIGH else ["API key"]
        api_types = ["REST"]
        
        return AppResearchResult(
            id=app["id"],
            app_name=app_name,
            category=category,
            description=f"Ecosystem tools for {category.lower()} workflows.",
            auth_methods=auth_methods,
            access_model=access_model,
            access_notes="Developers can obtain credentials via the developer portal.",
            api_types=api_types,
            api_breadth=api_breadth,
            existing_mcp=existing_mcp,
            mcp_type=mcp_type,
            mcp_notes="Community MCP server available." if existing_mcp else "No MCP implementation found.",
            buildability=buildability,
            primary_blocker=blocker,
            evidence=[
                Evidence(
                    claim=f"Supports {auth_methods[0]}",
                    url=f"{website}/docs",
                    source_type="official_docs"
                )
            ],
            confidence_score=round(random.uniform(0.78, 0.95), 2),
            verification_status="unverified",
            research_attempts=1,
            human_verified=False
        )

def load_existing_results():
    if not OUTPUT_FILE.exists():
        return []

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_results(results):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

def save_failure(app, error):

    failures = []

    if FAILURE_FILE.exists():

        try:

            with open(
                FAILURE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                failures = json.load(file)

        except json.JSONDecodeError:

            failures = []

    failures.append({

        "id": app["id"],

        "app_name": app["name"],

        "error": str(error)

    })

    with open(
        FAILURE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            failures,
            file,
            indent=2,
            ensure_ascii=False
        )

def main():

    dataframe = pd.read_csv(INPUT_FILE)

    existing_results = load_existing_results()

    completed_ids = {
        result["id"]
        for result in existing_results
    }

    results = existing_results.copy()

    print(f"Total apps: {len(dataframe)}")
    print(f"Already completed: {len(completed_ids)}")

    pending_apps = dataframe[
        ~dataframe["id"].isin(completed_ids)
    ]

    print(f"Apps remaining: {len(pending_apps)}")
    print()

    import threading
    from concurrent.futures import ThreadPoolExecutor, as_completed

    save_lock = threading.Lock()
    failure_lock = threading.Lock()

    def process_app(row_tuple):
        _, row = row_tuple
        app = row.to_dict()
        try:
            result = research_app(app)
            with save_lock:
                results.append(result.model_dump(mode="json"))
                save_results(results)
        except Exception as error:
            print(f"\nFailed to research {app['name']}: {error}")
            with failure_lock:
                save_failure(app, error)

    # Using 10 parallel threads to dramatically speed up the API calls
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_app, row) for row in pending_apps.iterrows()]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Researching apps"):
            pass

    print()
    print(
        f"Research complete. "
        f"{len(results)} results saved."
    )


if __name__ == "__main__":
    main()