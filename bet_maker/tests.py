from unittest import mock

import pytest
from httpx import AsyncClient

from bet_maker.application import app, container
from bet_maker.services import Service

BETS = [
    {
        "bet_id": "994af65b-e8af-4972-a58d-4255a5f06a8c",
        "event_id": "1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed",
        "amount": "30",
        "status": "WIN"},
    {
        "bet_id": "035e6ee6-09ee-408e-b12a-66f87e60f928",
        "event_id": "550e8400-e29b-41d4-a716-446655440000",
        "amount": "14.0",
        "status": "LOSE"
    },
]


@pytest.fixture
def client(event_loop):
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    event_loop.run_until_complete(client.aclose())


@pytest.mark.asyncio
async def test_get_bets(client):
    service_mock = mock.AsyncMock(spec=Service)
    service_mock.get_hash_values.return_value = BETS

    with container.service.override(service_mock):
        response = await client.get("/bets")

    assert response.status_code == 200
    assert response.json() == {"result": BETS}
