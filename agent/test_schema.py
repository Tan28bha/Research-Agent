from schemas import AppResearchResult


sample = {
    "id": 1,
    "app_name": "Salesforce",
    "category": "CRM and Sales",
    "description": "Cloud CRM platform.",
    "auth_methods": [
        "OAuth2"
    ],
    "access_model": "self_serve_free",
    "access_notes": (
        "Developer accounts can create connected apps."
    ),
    "api_types": [
        "REST",
        "SOAP"
    ],
    "api_breadth": "broad",
    "existing_mcp": False,
    "mcp_type": "none",
    "mcp_notes": "",
    "buildability": "high",
    "primary_blocker": "none",
    "evidence": [
        {
            "claim": "Supports OAuth2",
            "url": "https://example.com",
            "source_type": "official_docs"
        }
    ],
    "confidence_score": 0.92
}


result = AppResearchResult(**sample)

print(result)
print()
print("Schema validation successful.")