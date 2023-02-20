import coc
import settings
import asyncio

@coc.ClanEvents.member_join()
async def member_join(member: coc.ClanMember, new_clan: coc.Clan):
    clan_tasks = []
    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.CLAN_CLIENTS.remove(ws)
            except:
                pass

    json_data = {"type": "member_join", "member": member._raw_data,
                 "clan": new_clan._raw_data}

    for client in settings.CLAN_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)

@coc.ClanEvents.member_leave()
async def member_leave(member: coc.ClanMember, new_clan: coc.Clan):
    clan_tasks = []
    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.CLAN_CLIENTS.remove(ws)
            except:
                pass

    json_data = {"type": "member_leave", "member": member._raw_data,
                 "clan": new_clan._raw_data}

    for client in settings.CLAN_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)

@coc.ClanEvents.member_donations()
async def member_donos(old_member: coc.ClanMember, new_member: coc.ClanMember):
    clan_tasks = []
    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.CLAN_CLIENTS.remove(ws)
            except:
                pass

    json_data = {"type": "member_donations", "old_member": old_member._raw_data,
                 "new_member": new_member._raw_data}

    for client in settings.CLAN_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)

@coc.ClanEvents.member_received()
async def member_received(old_member: coc.ClanMember, new_member: coc.ClanMember):
    clan_tasks = []
    async def send_ws(ws, json):
        try:
            await ws.send_json(json)
        except:
            try:
                settings.CLAN_CLIENTS.remove(ws)
            except:
                pass

    json_data = {"type": "member_received", "old_member": old_member._raw_data,
                 "new_member": new_member._raw_data}

    for client in settings.CLAN_CLIENTS.copy():
        task = asyncio.ensure_future(send_ws(ws=client, json=json_data))
        clan_tasks.append(task)
    await asyncio.gather(*clan_tasks, return_exceptions=False)