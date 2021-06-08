import os
import discord
from discord.errors import Forbidden, HTTPException, InvalidArgument
from discord.ext import commands


# ID's
CHANNEL_ID = 849081782367420416
ADMIN_ID = 790305335927635980
SPECIAL_ID = 790574118046400533


# Set bot permissions
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)


# Confirm the bot is live
@client.event
async def on_ready():
    print('Bot is online.')


# Refactored method for sending dm's to admins
async def send_admin_dms(member, message):

    # Get the admin role
    guild = member.guild

    # Get the admin role
    admin_role = guild.get_role(ADMIN_ID)

    # Exit if it could not be found
    if admin_role is None:
        print('The admin role could not be found.')
        return

    # Send message to all admins
    admins = admin_role.members
    for admin in admins:

        # Create a dm if one does not already exist
        if admin.dm_channel is None:
            await admin.create_dm()

        # Send dm message
        dm = admin.dm_channel
        try:
            await dm.send(message)

        except HTTPException:
            print('A DM failed to send.')

        except Forbidden:
            print('Bot does not have permission to send DMs.')

        except InvalidArgument:
            print('This should not ever happen.')


# DM admins if a member joins the server
@client.event
async def on_member_join(member):
    await send_admin_dms(member, f'{member.name} has joined Valhalla.')


# DM admins if a member leaves the server
@client.event
async def on_member_remove(member):
    await send_admin_dms(member, f'{member.name} has left Valhalla.')


# Send a message to the channel if someone gets the special role
@client.event
async def on_member_update(before, after):

    # Get the guild
    guild = after.guild

    # Get the role
    special_role = guild.get_role(SPECIAL_ID)

    # Exit if it could not be found
    if special_role is None:
        print('The special role could not be found.')
        return

    # Exit if the member does not have the special role after
    for role in after.roles:
        if role == special_role:
            break
    else:
        return

    # Exit if the member already had the role
    for role in before.roles:
        if role == special_role:
            return   

    # Get the channel
    channel = guild.get_channel(CHANNEL_ID)

    # Exit if it could not be found
    if channel is None:
        print('The channel could not be found.')
        return

    # Send the message
    await channel.send(f'Pour the mead and welcome our new Valhallan!\n{after.mention}, we are thrilled to have you.\nPlease introduce yourself when able, we would love to get to know you!')


# Run Bot
client.run(os.environ.get('BOT_TOKEN'))
