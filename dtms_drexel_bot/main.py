import os
import discord 
from discord.ext import commands
from dotenv import load_dotenv
from dtms_client.DMTSClient import DTMSClient

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = DTMSClient("https://dtms.shahriyarshawon.xyz/")
bot = commands.Bot(command_prefix='./', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def getclass(ctx, *, course_number: str):
    print(f"Getting class {course_number}")
    drexel_class = client.get_class(course_number)
    embed = discord.Embed(title=drexel_class.number, description=drexel_class.name, color=discord.Color.dark_blue())
    embed.add_field(name = "Description", value = drexel_class.desc, inline=False)
    embed.add_field(name = "Credits", value = drexel_class.high_credits, inline=False)
    embed.add_field(name = "Writing Intensive", value = drexel_class.writing_intensive, inline=False)
    embed.add_field(name = "Prerequesites", value = drexel_class.prereqs, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def prereqsfor(ctx, *, course_number: str):
    print(f"Getting class {course_number}")
    #drexel_class = client.get_class(course_number)
    prereq_paths = client.get_prereqs_for_class(course_number)
    #embed = discord.Embed(title=drexel_class.number, description=drexel_class.name, color=discord.Color.dark_blue())
    #embed.add_field(name = "Prerequesites", value = "\n".join(prereq_paths), inline=False)
    prereq_paths_str = "\n".join(prereq_paths)
    await ctx.send(f"""```md\n{prereq_paths_str}```""")

@bot.command()
async def postreqsfor(ctx, *, course_number: str):
    print(f"Getting class {course_number}")
    postreqs = client.get_postreqs_for_class(course_number)
    postreqs_str = "\n".join(postreqs)
    await ctx.send(f"""```md\n{postreqs_str}```""")


load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))