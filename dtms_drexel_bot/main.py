import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from dtms_client.DMTSClient import DTMSClient
import argparse

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = DTMSClient("https://dtms.shahriyarshawon.xyz/")
bot = commands.Bot(command_prefix="./", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def getcourse(ctx, *, course_number: str):
    print(f"Getting class {course_number}")
    drexel_class = client.get_class(course_number)
    embed = discord.Embed(
        title=drexel_class.number,
        description=drexel_class.name,
        color=discord.Color.dark_blue(),
    )
    embed.add_field(name="Description", value=drexel_class.desc, inline=False)
    embed.add_field(name="Credits", value=drexel_class.high_credits, inline=False)
    embed.add_field(
        name="Writing Intensive", value=drexel_class.writing_intensive, inline=False
    )
    embed.add_field(name="Prerequesites", value=drexel_class.prereqs, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def prereqs(ctx, *, course_number: str):
    print(f"Getting class {course_number}")
    prereq_paths = client.get_prereqs_for_class(course_number)
    prereq_paths_str = "\n".join(prereq_paths)
    await ctx.send(f"""```md\n{prereq_paths_str}```""")


@bot.command()
async def postreqs(ctx, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--course", help="Course to find postreqs for. ex MATH 201"
    )
    parser.add_argument(
        "-s", "--subject-filter", help="Subject to filter results by. ex1 CS or ECE"
    )
    args = parser.parse_args(args)
    if args.course is None:
        await ctx.send(f"```{parser.format_help()}```")
        return
    print(f"Getting class {args.course}")
    postreqs = client.get_postreqs_for_class(
        args.course, subject_filter=args.subject_filter.upper()
    )
    postreqs_str = "\n".join(postreqs)
    await ctx.send(f"""```md\n{postreqs_str}```""")


@bot.command()
async def tmssearch(ctx, term: str, *args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--college")
    parser.add_argument("--subject")
    parser.add_argument("--credit-hours")
    parser.add_argument("--prereq")
    parser.add_argument("--instructor")
    parser.add_argument("--writing-intensive")
    args = parser.parse_args(args)
    courses = client.get_classes_for_term(
        term,
        college=args.college,
        subject=args.subject,
        credit_hours=args.credit_hours,
        prereq=args.prereq,
        instructor=args.instructor,
        writing_intensive=args.writing_intensive,
    )
    courses = "\n".join([course.course_number for course in courses])
    await ctx.send(f"""```md\n{courses}```""")


load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))
