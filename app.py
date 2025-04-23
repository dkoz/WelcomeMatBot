import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = 849081782367420416
ADMIN_ID = 814669164626313226
SPECIAL_ID = 790574118046400533

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=os.getenv("BOT_PREFIX", "!"), intents=intents)

@bot.event
async def on_ready():
    print('Bot is online.')

async def send_admin_dms(member, message):
    guild = member.guild
    admin_role = guild.get_role(ADMIN_ID)
    if admin_role is None:
        print('The admin role could not be found.')
        return
    for admin in admin_role.members:
        if admin.dm_channel is None:
            await admin.create_dm()
        dm = admin.dm_channel
        try:
            await dm.send(message)
        except discord.HTTPException:
            print('A DM failed to send.')
        except discord.Forbidden:
            print('Bot does not have permission to send DMs.')
        except discord.InvalidArgument:
            print('This should not ever happen.')

@bot.event
async def on_member_join(member):
    await send_admin_dms(member, f'{member.name} has joined Valhalla.')

@bot.event
async def on_member_remove(member):
    await send_admin_dms(member, f'{member.name} has left Valhalla.')
    guild = member.guild
    special_role = guild.get_role(SPECIAL_ID)
    if special_role is None:
        print('The special role could not be found.')
        return
    for role in member.roles:
        if role == special_role:
            break
    else:
        return
    channel = guild.get_channel(CHANNEL_ID)
    if channel is None:
        print('The channel could not be found.')
        return
    await channel.send(f'{member.name} has departed Valhalla.')

@bot.event
async def on_member_update(before, after):
    guild = after.guild
    special_role = guild.get_role(SPECIAL_ID)
    if special_role is None:
        print('The special role could not be found.')
        return
    for role in after.roles:
        if role == special_role:
            break
    else:
        return
    for role in before.roles:
        if role == special_role:
            return
    channel = guild.get_channel(CHANNEL_ID)
    if channel is None:
        print('The channel could not be found.')
        return
    await channel.send(f'Pour the mead and welcome our new Valhallan!\n{after.mention}, we are thrilled to have you.\nPlease introduce yourself when able, we would love to get to know you!')

bot.run(os.getenv("BOT_TOKEN"))