import discord
import myToken
import nico2
import musicPlayer
import time

client = discord.Client()
nc = nico2.nico2py()
vc:discord.VoiceClient = None
mp = musicPlayer.musicPlayer()

status = { "playing":0, "stop":1, "pause":2 }
nowStatus = status["stop"]

@client.event
async def on_ready():
    print("nicoRythm Logged in")
    print( client.user.name )
    print( client.user.id )
    print("-------------------")

@client.event
async def on_message(message):

    global vc
    global nc
    global status
    global nowStatus
    
    if message.content == "e":
        await client.logout()
    
    elif message.content.startswith("#play"):

        if vc == None:
            voice_ch = message.author.voice.channel
            vc = await voice_ch.connect()
            await message.channel.send( "connect!" )

        # キュー追加
        if message.content.find( "https://www.nicovideo.jp/watch/sm" ) >= 0 :
            mp.addQueue( message.content.split(" ")[1] )

        # 停止中か
        if nowStatus == status["stop"]:    
            
            nowStatus = status["playing"]
            mp.play()
            vc.play(  discord.FFmpegPCMAudio(  nc.getVideo( mp.nowPlaying["url"] ) ) )
            vc.source = discord.PCMVolumeTransformer( vc.source )
            vc.source.volume = 0.05
            await message.channel.send( mp.now() )
        
        elif nowStatus == status["pause"]:
            nowStatus = status["playing"]
            vc.play( vc.sourse )

    elif message.content == "#stop":

        # 1時停止
        vc.pause()
        nowStatus = status["pause"]
        await message.channel.send( "stop" )

    elif message.content == "#skip":
        
        vc.stop()
        nc.isDownload = False
        time.sleep(1)
        mp.play()
        nowStatus = status["stop"]
        await message.channel.send( "skip" )

        if mp.nowPlaying["url"] != None:
            vc.play(  discord.FFmpegPCMAudio(  nc.getVideo( mp.nowPlaying["url"] ) ) )
            vc.source = discord.PCMVolumeTransformer( vc.source )
            vc.source.volume = 0.05
            nowStatus = status["playing"]
            await message.channel.send( mp.now() )

    elif message.content == "#queue":
        
        await message.channel.send( mp.showQueue() )

    elif message.content.startswith("#remove"):

        if int( message.content.split(" ")[1] ) >= 0:
            m = "remove {0}".format( mp.playQueue[ int( message.content.split(" ")[1]) ]["title"] )
            mp.removeQueue( int( message.content.split(" ")[1] ) )
            await message.channel.send( m )
        
        else:
            await message.channel.senf( "error invalid index" )

    elif message.content == "dc":
        await vc.disconnect()
        vc = None
        await message.channel.send("disconnect")

client.run( myToken.discord_token )