import uuid
from decimal import Decimal
from enum import Enum

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from .containers import Container
from .services import Service


class StatusEnum(str, Enum):
    win = 'WIN'
    lose = 'LOSE'
    not_finished = 'NOT_FINISHED'


class Bet(BaseModel):
    event_id: uuid.UUID
    amount: Decimal
    status: StatusEnum = StatusEnum.not_finished


class Event(BaseModel):
    status: StatusEnum = StatusEnum.not_finished


app = FastAPI()


@app.post("/bets")
@inject
async def create_bet(bet: Bet, service: Service = Depends(Provide[Container.service])):
    bet_id = uuid.uuid4()
    await service.set_value(f"bets:{bet_id}", {"bet_id": str(bet_id), "event_id": str(bet.event_id), "amount": str(bet.amount), "status": bet.status})
    await service.add_index(f"event_id:{bet.event_id}", str(bet_id))
    return {"result": {"bet_id": bet_id}}


@app.get("/bets")
@inject
async def get_bets(service: Service = Depends(Provide[Container.service])):
    bets = await service.get_hash_values("bets:*")
    return {"result": bets}


@app.put("/events/{event_id}")
@inject
async def change_event(event_id: str, event: Event, service: Service = Depends(Provide[Container.service])):
    bet_ids = await service.get_set_values(f"event_id:{event_id}")
    keys = [f"bets:{bet_id}" for bet_id in bet_ids]
    await service.change_field_value(keys, {"status": event.status})
    return {"result": bet_ids}


container = Container()
container.config.redis_host.from_env("REDIS_HOST", "localhost")
container.config.redis_password.from_env("REDIS_PASSWORD", "password")
container.wire(modules=[__name__])
