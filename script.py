from v2 import test2
import asyncio 


async def test():
    print('test')
    asyncio.run(test2())

asyncio.run(test())