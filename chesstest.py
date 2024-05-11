import asyncio

import chessdotcom

chessdotcom.Client.request_config["headers"]["User-Agent"] = (
   "My Python Application. "
   "Contact me at email@example.com"
)

leaderboard = chessdotcom.client.get_leaderboards().json['leaderboards']

print(leaderboard['live_blitz'][:5])