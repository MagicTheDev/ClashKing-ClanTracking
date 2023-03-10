import coc
import sys
sys.path.append("..")
import settings
import asyncio

@coc.WarEvents.new_war()
async def new_war(new_war: coc.ClanWar):
    clan_tasks = []
    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.WAR_CLIENTS.remove(ws)
            except:
                pass

    league_group = None
    if new_war.is_cwl:
        league_group: coc.ClanWarLeagueGroup = new_war.league_group
        league_group = league_group._raw_data

    json_data = {"type": "new_war", "war": new_war._raw_data, "league_group" : league_group}

    for client in settings.WAR_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)

@coc.WarEvents.war_attack()
async def war_attack(attack: coc.WarAttack, war: coc.ClanWar):
    clan_tasks = []
    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.WAR_CLIENTS.remove(ws)
            except:
                pass

    json_data = {"type": "war_attack", "attack": attack._raw_data, "war": war._raw_data}

    for client in settings.WAR_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)