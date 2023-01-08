import discord
from discord.ext import commands
import wavelink


client = commands.Bot(command_prefix='!',intents=discord.Intents.all())
client.remove_command("help")

@client.event
async def on_ready():
    client.loop.create_task(connect_nodes())
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Howl'))
    print('Bot is online!')
    
    
async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client, host='node1.kartadharta.xyz', port=443, password='kdlavalink', https=True
    )
    
    
@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f'Node: <{node.identifier}> is ready!')
    
    
@client.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.YouTubeTrack, reason):


  ctx = player.ctx
  vc: player = ctx.voice_client


  if vc.loop:
    return await vc.play(track)

  if vc.queue.is_empty:
    emd = discord.Embed(title="", description="**Queue is empty so i left the voice channel**")
    await ctx.send(embed = emd)
    return await vc.disconnect()

  next_song = vc.queue.get()
  await vc.play(next_song)
  em = discord.Embed(title="Now Playing", description=f"{next_song.title}")
  await ctx.send(embed = em)
  
  thumbnail: str
@client.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
  if not ctx.voice_client:
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.send("join a voice channel first")
  else:
    vc: wavelink.Player = ctx.voice_client

  if vc.queue.is_empty and not vc.is_playing():
      await vc.play(search)
      embed = discord.Embed(title="Now Playing", description=f"{search.title}")
      await ctx.send(embed = embed)
