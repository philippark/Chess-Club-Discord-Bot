import asyncio

from chessdotcom import get_player_profile, Client

Client.aio = True

async def profile():
    response = await asyncio.gather(get_player_profile("philipparko"))
    return response

print(asyncio.run(profile()))