from discord.ext import commands
from discord import app_commands
import discord
import requests
import json
from keys import BOT_TOKEN
from keys import WEATHER_API


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
quotes_file = "Quote_Bot/Quotes.csv" #remember to change / to \ in file path when not in use on server

#Quote Command
@tree.command(
    name="weather",
    description="Generate a 3 day weather forecast"
)
async def first_command(interaction, location: str):

    try:
        URL = "http://api.weatherapi.com/v1/forecast.json"
        params = {"key": WEATHER_API, 
            "q": location, 
            "days" : 3, 
            "hour": 17}
        
        response = requests.get(URL, params)
        results = response.json()["forecast"]["forecastday"]
        strng_lst = []
        
        for result in results:
            strng_lst.append(f"""**Date:** {result['date']}, 
    **Average Temp(f):** {result['day']['avgtemp_f']} 
    **Average Temp(c):** {result['day']['avgtemp_c']} 
    **Chance of rain:** {result['day']['daily_chance_of_rain']}%
    **Chance of snow:** {result['day']['daily_chance_of_snow']}%
    --------------------""")
        final_message = "\n".join(strng_lst)
        await interaction.response.send_message(f"""Weather for {location}: 
    {final_message}""")
    except:
        await interaction.response.send_message("""Something didnt didnt quite work there, check your spelling and try again!
    if the issue persists then speak with @boniface""")

#Bot Ready Event
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(BOT_TOKEN)