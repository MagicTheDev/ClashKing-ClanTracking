import coc
import sys
sys.path.append("..")
import settings
import asyncio

@coc.RaidEvents.new_offensive_opponent()
async def new_opponent(clan: coc.RaidClan, raid: coc.RaidLogEntry):
    clan_tasks = []

    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.RAID_CLIENTS.remove(ws)
            except:
                pass

    json_data = {"type": "new_raid_opponent", "clan_tag" : raid.clan_tag, "clan": clan._raw_data, "raid": raid._raw_data}

    for client in settings.RAID_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)


@coc.RaidEvents.raid_attack()
async def raid_attack(attack: coc.RaidAttack, raid: coc.RaidLogEntry):
    clan_tasks = []

    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.RAID_CLIENTS.remove(ws)
            except:
                pass

    json_data = {"type": "raid_attacks", "clan_tag" : raid.clan_tag, "attack": attack._raw_data, "raid": raid._raw_data}

    for client in settings.RAID_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)
