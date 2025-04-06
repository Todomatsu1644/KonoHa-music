import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# queue
queue = []

@bot.event
async def on_ready():
    print(f"Бот ажиллаж байна: {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Дууны сувагт нэвтэрлээ!")
    else:
        await ctx.send("Та эхлээд дуут сувагт нэвтэрнэ үү!")

@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('join'))

    queue.append(url)
    if not ctx.voice_client.is_playing():
        await play_next(ctx)

async def play_next(ctx):
    if len(queue) == 0:
        await ctx.send("Queue хоосон байна.")
        return

    url = queue.pop(0)

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
        'cookiefile': 'cookies.txt',  # <-- ЭНЭ МӨР ШИНЭЭР НЭМЭГДЭНЭ
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

    ctx.voice_client.play(discord.FFmpegPCMAudio(filename), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
    await ctx.send(f"🎶 Тоглуулж байна: {info['title']}")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭ Дараагийн дуу руу шилжлээ.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Гарлаа.")
    else:
        await ctx.send("Би одоогоор ямар ч дуут сувагт байхгүй.")
# Bot-ын TOKEN-оо энд бичнэ
bot.run("YOUR_BOT_TOKEN")


source = discord.FFmpegPCMAudio(audio_url, executable="ffmpeg", **FFMPEG_OPTIONS)
