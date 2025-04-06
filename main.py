import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} ажиллаж байна!")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Та эхлээд дууны сувагт орно уу!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Би ямар ч суваг дээр холбогдоогүй байна.")

@bot.command()
async def play(ctx, url):
    if ctx.voice_client is None:
        await ctx.send("Эхлээд `!join` командыг ашиглаад намайг сувгаа холбож өгнө үү.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True
    }

    ffmpeg_opts = {
        'options': '-vn'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            source = discord.FFmpegPCMAudio(audio_url, executable="ffmpeg", **ffmpeg_opts)
            ctx.voice_client.play(source)
            await ctx.send(f"🎵 Тоглож байна: {info['title']}")
    except Exception as e:
        await ctx.send(f"⚠️ Алдаа гарлаа: {str(e)}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ Дуу зогсоолоо.")
    else:
        await ctx.send("Одоогоор ямар ч дуу тоглогдоогүй байна.")

# Bot-г эхлүүлэх
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
