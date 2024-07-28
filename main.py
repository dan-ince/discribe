import discord
from discord.ext import commands
import assemblyai as aai

aai.settings.api_key = "e8e9d08830f74973ae9156162d3bae4d"
transcriber = aai.Transcriber()
config = aai.TranscriptionConfig()

TOKEN = 'MTI2Njg3MDQzNjY1OTIwNDEyOA.G9iJZo.U30pU6EnNtuwHeyxyYI9upiXQzBhHM-KMnGeR4'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True

responded_messages = set()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('audio/'):
                # React to the message with an emoji, for example, a checkmark
                await message.add_reaction('💬')
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    # Ensure the bot doesn't respond to its own reactions
    if user == bot.user:
        return
    
    # Check if the reaction is on a message with an audio attachment and the emoji is the one we added
    if reaction.emoji == '💬':
        for attachment in reaction.message.attachments:
            if attachment.content_type and attachment.content_type.startswith('audio/'):
                # Reply to the message with the username of the person who added the reaction
                if reaction.message.id not in responded_messages:
                    responded_messages.add(reaction.message.id)
                    initial_reply = await reaction.message.reply('```Transcribing...```')
                    transcript = transcriber.transcribe(attachment.url)
                    await initial_reply.edit(content=f'**{reaction.message.author.name}**: ```{transcript.text}```')

bot.run(TOKEN)
