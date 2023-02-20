import os
import coc
from uvicorn import Config, Server
from fastapi import FastAPI, WebSocket, Depends, Query, WebSocketDisconnect
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import motor.motor_asyncio
import asyncio
import pytz
import clan_events
from clash import setup_coc, clash_client
import settings


utc = pytz.utc
app = FastAPI()



@app.on_event("startup")
async def startup_event():
    await setup_coc()

db_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("DB_LOGIN"))
usafam = db_client.usafam
clan_db = usafam.clans

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:mvalerya12@104.251.216.53:27017/admin?readPreference=primary&directConnection=true&ssl=false&authMechanism=DEFAULT&authSource=admin")
new_looper = client.new_looper
player_stats = new_looper.player_stats

clan_tags = asyncio.get_event_loop().run_until_complete(clan_db.distinct("tag"))
clash_client.add_clan_updates(*clan_tags)

@app.websocket("/clans")
async def player_websocket(websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    settings.CLAN_CLIENTS.add(websocket)
    try:
        '''Authorize.jwt_required("websocket", token=token)
        await websocket.send_text("Successfully Login!")
        decoded_token = Authorize.get_raw_jwt(token)
        await websocket.send_text(f"Here your decoded token: {decoded_token}")'''
        try:
            while True:
                data = await websocket.receive_text()
        except WebSocketDisconnect:
            settings.CLAN_CLIENTS.remove(websocket)
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()


@coc.ClientEvents.clan_loop_start()
@coc.ClientEvents.raid_loop_start()
@coc.ClientEvents.war_loop_start()
async def start(iter_spot):
    if iter_spot % 10 == 0:
        clan_tags = await clan_db.distinct("tag")
        #db_tags = await player_stats.distinct("clan_tag")
        #clan_tags = list(set(clan_tags + db_tags))
        clash_client.add_clan_updates(*clan_tags)


#add events
clash_client.add_events(start, clan_events.member_join, clan_events.member_leave, clan_events.member_donos, clan_events.member_received)

loop = asyncio.get_event_loop()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
config = Config(app=app, loop="asyncio", ws_ping_interval=3600, ws_ping_timeout=3600, timeout_keep_alive=3600, timeout_notify=3600)
server = Server(config)
loop.create_task(server.serve())
loop.run_forever()


