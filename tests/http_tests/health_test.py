
import pytest
from httpx import AsyncClient, ASGITransport

from fastapi import FastAPI

from app.api.v1.check import router

app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio(loop_scope='function')
async def test_get_health():
    """
    Test the health endpoint
    :return:
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}