import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord import FFmpegOpusAudio
from ElevenLabsTTS import text_to_speech # This uses ElevenLabs' TTS
from Mistralchatbot import chatbot # This uses Mistral's chatbot
from googleTTS import googleTTS # This uses Google's TTS
from openAIchatbot import simplechat # This uses OpenAI's chatbot

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


# Load variables from the .env file
load_dotenv()
# Access the variables
discordAPI = os.getenv("DISCORD")
# Bot setup
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        # Get the voice channel the author of the command is in
        channel = ctx.message.author.voice.channel

        # Connect to the voice channel
        await channel.connect()

    else:
        await ctx.send("You are not in a voice channel")

@bot.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        # Disconnect from the voice channel
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am currently not in a voice channel")
        
conversation = []

@bot.command(pass_context = True)
async def ask(ctx):
    global conversation
    inputpormpt = ctx.message.content[5:]
    file_path_audio = 'output.mp3'
    print("Have inputed:",inputpormpt)
    # Call Chatbot
    output_text, conversation = simplechat(message=inputpormpt,conversation=conversation)
    print("Output from model:", output_text)
    # Check to see if bot and user are in a vc
    if ctx.voice_client and ctx.author.voice:
        # Call TTS
        googleTTS(output_text)
        # Play TTS output
        voice = ctx.voice_client
        source = FFmpegOpusAudio(source=file_path_audio)
        await ctx.send(output_text)
        player = voice.play(source)
    else:
        await ctx.send(output_text)

bot.run(discordAPI)