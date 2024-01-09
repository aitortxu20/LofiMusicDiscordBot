import os
import discord
from discord.ext.commands import Bot
import yt_dlp as youtube_dl
import ffmpeg
from discord import FFmpegPCMAudio, FFmpegAudio

from dotenv import load_dotenv
import asyncio

load_dotenv()

my_secret = os.getenv('TOKEN')
intents = discord.Intents.all()
a = 0
bot = Bot(command_prefix='/', intents=intents)

video_links = [
  "https://www.youtube.com/watch?v=oQnV2UqJMrw",
  "https://www.youtube.com/watch?v=_4kLioMoMrk",
  "https://www.youtube.com/watch?v=8nXqcugV2Y4",
  "https://www.youtube.com/watch?v=0ucdLWYhdAc",
  "https://www.youtube.com/watch?v=f02mOEt11OQ",
  "https://www.youtube.com/watch?v=SigIbCVMTzU",
  "https://www.youtube.com/watch?v=UokZMBmnUGM",
  "https://www.youtube.com/watch?v=_ITiwPMUzho",
]

ydl_opts = {
  'format': 'bestaudio/best',
  'extractaudio': True,
  'audioformat': 'mp3',
  'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
  'restrictfilenames': True,
  'noplaylist': True,
  'nocheckcertificate': True,
  'ignoreerrors': False,
  'logtostderr': False,
  'quiet': True,
  'no_warnings': True,
  'default_search': 'auto',
  'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
  'before_options':
  '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn'
}


@bot.event
async def on_ready():

  activity = discord.Activity(type=discord.ActivityType.listening,
                              name="Lofi music")
  await bot.change_presence(status=discord.Status.idle, activity=activity)

@bot.event
async def on_voice_state_update(member, before, after):
  await asyncio.sleep(1)
  c = 0
  dfChannel = bot.get_channel(1177618746425217105)

  if after.channel != "Lofi 24/7" or after.channel is None:
    for miembro in dfChannel.members:
      c += 1
    if c == 1:
      for vc in bot.voice_clients:
        await vc.disconnect()

  if dfChannel:
    if after.channel == dfChannel:


      if after.channel.id == 1177618746425217105:

        channel = bot.get_channel(1177618746425217105)
        vc = await channel.connect()

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(video_links[0], download=False)
          URL = info['url']


          discord.opus.load_opus('./opus-1.3.1/.libs/libopus.so.0.8.0')

          if not vc.is_playing():

            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                    after=lambda e: play_next(vc))



  if after.channel.id == 1177618746425217105 and member.id != 1130234759675662346:
    await member.edit(mute=True)
  if after.channel.id != 1177618746425217105 or after.channel.id is None:
    await member.edit(mute=False)
  if after.channel is None and member == bot.user:
    channel = bot.get_channel(1177618746425217105)
    vc = await channel.connect()


def play_next(vc):
  pos_0 = video_links[0]

  for video_link in video_links:
    video_links.pop(0)
    video_links.append(pos_0)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(video_link, download=False)
      URL = info['url']

      discord.opus.load_opus('./opus-1.3.1/.libs/libopus.so.0.8.0')
      vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
              after=lambda e: play_next(vc))

bot.run(my_secret)
