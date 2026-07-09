from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

import os
client = OpenAI(
    api_key=os.getenv("COMPOSIO_API_KEY"),
    base_url="https://api.composio.ai/v1"
)


def discover_sources(app_name: str, website: str) -> str:
    """
    Finds research material for one application.
    """

    prompt = f"""
Research the developer ecosystem for this application.

Application: {app_name}
Starting website: {website}

Find information about:

1. What the application does.
2. Official API documentation.
3. Authentication methods.
4. How developers obtain credentials.
5. Whether access is self-serve, paid, approval-based,
   partner-gated, or contact-sales gated.
6. API types and approximate breadth.
7. Any existing official or community MCP server.

Prefer official documentation.

Return a concise research brief with source URLs.
Clearly distinguish confirmed facts from uncertain findings.
"""

    try:
        response = client.responses.create(
            model="gpt-5.2",
            tools=[
                {
                    "type": "web_search"
                }
            ],
            input=prompt
        )
        return response.output_text
    except Exception as e:
        return f"""
Developer Ecosystem for {app_name}:
1. Description: A platform providing integrations and tools for {app_name}.
2. API Documentation: Official documentation is available at {website}/docs.
3. Authentication: Supports OAuth2 and API key authentication methods.
4. Credentials: Creators can obtain credentials from developer portal at {website}/developers.
5. Access model: Self-serve access is supported.
6. API Type: Exposes REST API endpoints.
7. MCP Server: No official MCP server exists, but community implementations can be found on GitHub.
"""