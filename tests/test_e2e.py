import os
import requests

# End-to-end tests against the deployed Container App (uses live network).
# Set E2E_BASE_URL environment variable to override the target host.
# Base URL and origin for e2e tests
BASE = os.getenv("E2E_BASE_URL", "https://rca-tracker.whiteocean-65212696.westeurope.azurecontainerapps.io")
FRONTEND_ORIGIN = os.getenv("E2E_FRONTEND_ORIGIN", "https://black-sea-064252b03.3.azurestaticapps.net")
# Timeout (seconds) for network requests; can be overridden with E2E_TIMEOUT env var.
TIMEOUT = int(os.getenv("E2E_TIMEOUT", "30"))


def test_post_and_get_incident():
    """POST a new incident then GET the list and assert the item exists."""
    payload = {
        "title": "e2e-test",
        "severity": "P5",
        "description": "created by e2e test"
    }

    headers = {"Origin": FRONTEND_ORIGIN, "Content-Type": "application/json"}

    # POST the incident
    r = requests.post(f"{BASE}/incidents", json=payload, headers=headers, timeout=TIMEOUT)
    assert r.status_code in (200, 201), f"POST failed: {r.status_code} {r.text}"
    created = r.json()
    assert created.get("title") == payload["title"]

    # GET the list and ensure the created title is present
    r2 = requests.get(f"{BASE}/incidents", timeout=TIMEOUT)
    assert r2.status_code == 200
    items = r2.json()
    assert any(i.get("title") == payload["title"] for i in items), "Created incident not found in GET /incidents"
