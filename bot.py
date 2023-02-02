import discord
import responses
import re
import random
import os
from itertools import chain
from dotenv import load_dotenv
from PIL import Image, ExifTags

async def send_message(message, user_message, channel):
    conf_file=open("discord-uploader.conf","r")
    conf=conf_file.readlines()
    directory=conf[2]
    directory=re.findall("\[([A-Za-z1-9_\-/]+)\]",directory)[0]
    try:
        response,*files= responses.get_response(user_message)
        files=list(chain(*files))
        if files:
            for file in files:
                i=0
                size=os.path.getsize(directory+"/"+file)
                print(size)
                too_big=False
                while(size>=8000000):
                    image=Image.open(directory+"/"+file)
                    width,height=image.size
                    aspect_ratio=width/height
                    height=height-(i*100)
                    width=height*aspect_ratio
                    image=image.resize((int(width),height),Image.ANTIALIAS)
                    image.save(directory+"/"+"tmp"+file,optimize=True,quality=95)
                    size=os.path.getsize(directory+"/"+"tmp"+file)
                    i+=1
                    too_big=True
                if too_big:
                    await message.channel.send(file=discord.File(directory+"/"+"tmp"+file))
                    os.remove(directory+"/"+"tmp"+file)
                else:
                    await message.channel.send(file=discord.File(directory+"/"+file))
        await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '/':
            user_message = user_message[1:]
            await send_message(message, user_message,channel)

    

    client.run(TOKEN)