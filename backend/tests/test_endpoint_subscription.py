import json
import pytest
from httpx import AsyncClient
from backend.main import app


@pytest.mark.anyio
async def test_create_subscription():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/web/subscriptions/",
            content=json.dumps({"webhook_url": "value", "feed_url": "test"}),
        )
    assert response.status_code == 201
    response = response.json()
    assert len(response) > 0
    assert response["id"] is not None
