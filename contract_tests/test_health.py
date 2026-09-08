import httpx


def test_health_returns_200(client: httpx.Client) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
