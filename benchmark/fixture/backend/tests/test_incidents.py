import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.mark.parametrize(("tenant", "total"), [("alpha", 18), ("beta", 9)])
def test_page_is_scoped_to_the_requested_tenant(tenant: str, total: int) -> None:
    response = client.get("/api/incidents", headers={"X-Tenant-ID": tenant})

    assert response.status_code == 200
    page = response.json()
    assert page["total"] == total
    assert page["page"] == 1
    assert page["page_size"] == 5
    assert len(page["items"]) == 5
    assert all(item["id"].startswith(f"{tenant}-") for item in page["items"])
    assert page["items"][0]["id"] == f"{tenant}-{total:03d}"


def test_pagination_preserves_total_and_returns_an_empty_out_of_range_page() -> None:
    headers = {"X-Tenant-ID": "alpha"}
    first = client.get("/api/incidents?page=1&page_size=2", headers=headers).json()
    second = client.get("/api/incidents?page=2&page_size=2", headers=headers).json()
    empty = client.get("/api/incidents?page=20&page_size=2", headers=headers).json()

    assert [item["id"] for item in first["items"]] == ["alpha-018", "alpha-017"]
    assert [item["id"] for item in second["items"]] == ["alpha-016", "alpha-015"]
    assert second["total"] == first["total"] == empty["total"] == 18
    assert empty["items"] == []


@pytest.mark.parametrize("query", ["page=0", "page=abc", "page_size=0", "page_size=51"])
def test_invalid_pagination_is_rejected(query: str) -> None:
    response = client.get(f"/api/incidents?{query}", headers={"X-Tenant-ID": "alpha"})
    assert response.status_code == 422


def test_unknown_and_missing_tenants_are_rejected() -> None:
    assert client.get("/api/incidents", headers={"X-Tenant-ID": "other"}).status_code == 401
    assert client.get("/api/incidents").status_code == 401
