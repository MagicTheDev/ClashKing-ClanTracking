import os

import coc
from uvicorn import Config, Server
from fastapi import FastAPI, WebSocket, Depends, Request, HTTPException, Query, WebSocketDisconnect, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import motor.motor_asyncio
import asyncio
import pytz

keys = []
utc = pytz.utc

from clash import setup_coc, client

async def main(app):
    @app.on_event("startup")
    async def startup_event():
        await setup_coc()

    CLAN_CLIENTS = set()
    @app.websocket("/clans")
    async def player_websocket(websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()):
        await websocket.accept()
        CLAN_CLIENTS.add(websocket)
        try:
            '''Authorize.jwt_required("websocket", token=token)
            await websocket.send_text("Successfully Login!")
            decoded_token = Authorize.get_raw_jwt(token)
            await websocket.send_text(f"Here your decoded token: {decoded_token}")'''
            try:
                while True:
                    data = await websocket.receive_text()
            except WebSocketDisconnect:
                CLAN_CLIENTS.remove(websocket)
        except AuthJWTException as err:
            await websocket.send_text(err.message)
            await websocket.close()

    db_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("DB_LOGIN"))
    usafam = db_client.usafam
    clan_db = usafam.clans

    clan_tags = await clan_db.distinct("tag")
    client.add_clan_updates(*clan_tags)

    @coc.ClanEvents.member_count()
    async def member_count_change(old_clan: coc.Clan, new_clan: coc.Clan):
        print(new_clan.member_count - old_clan.member_count)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = FastAPI()
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    config = Config(app=app, loop="asyncio", ws_ping_interval=3600, ws_ping_timeout=3600, timeout_keep_alive=3600, timeout_notify=3600)
    server = Server(config)
    loop.create_task(server.serve())
    loop.create_task(main(app))
    loop.run_forever()


