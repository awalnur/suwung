import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.api import init_routers

app = FastAPI()

init_routers(app)

@pytest.mark.asyncio(loop_scope='function')
async def test_authenticate():
    """
    Test the authentication endpoint
    :return:
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/v1/auth/token")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
