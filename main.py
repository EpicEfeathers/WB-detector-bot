# Discord imports
import discord
from discord.ext import tasks
import requests
import time

online = False

activity = discord.Activity(name = "my activity", type = discord.ActivityType.custom, state = "Tracking Players")

# MyClient class
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, activity: discord.Activity):
        super().__init__(intents=intents,activity=activity)

    @tasks.loop(seconds=10)
    async def check_online(self):
        global online
        response = requests.get("https://wbapi.wbpjs.com/players/getPlayer?uid=609aa68ed142afe952202c5c")
        last_seen = response.json()["time"]
        current_time = round(time.time())
        difference = current_time - last_seen
        
        channel = self.get_channel(1287401466939703316)
        if difference <= 30:
            if not online:
                await channel.send(f"Came online at <t:{last_seen}:t>")
                online = True
        else:
            if online:
                await channel.send(f"Came offline at <t:{last_seen}:t>")
                online = False

intents = discord.Intents.default()
client = MyClient(intents=intents,activity=activity)

# When bot boots
@client.event
async def on_ready():
    try:
        client.check_online.start()
    except: # running already
        pass
    print(f"Successfully logged in as \033[1m{client.user}\033[0m")    
