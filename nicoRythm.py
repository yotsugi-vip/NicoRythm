import discord
import myToken
import nico2
import musicPlayer
import time
import threading

client = discord.Client()
nc = nico2.nico2py()
vc:discord.VoiceClient = None
mQueue = musicPlayer.QueueCtrl()
isPlay = False

def playcheck( ):
    global vc
    global isPlay

    if isPlay:
        print("start")

    while isPlay:
        if vc.is_paused()  == False:
            time.sleep(0.5)
            if vc.is_playing() == False:
                mQueue.popQueue()
                src = nc.getVideo( mQueue.nowPlaying["url"] )
                time.sleep( 5 )
                vc.play( discord.FFmpegPCMAudio( src ) )
                vc.source = discord.PCMVolumeTransformer( vc.source )
                vc.source.volume = 0

            

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
    global isPlay
    t1 = threading.Thread( target=playcheck )

    if message.content == "e":
        await client.logout()
    
    elif message.content.startswith("#play"):

        # 接続処理
        if vc == None:
            voice_ch = message.author.voice.channel
            vc = await voice_ch.connect()
            await message.channel.send( "connect!" )
        
        if message.content == "#play":

            # 再開
            if vc.is_paused():
                vc.resume()

        # キュー追加
        elif message.content.find( "https://www.nicovideo.jp/watch/sm" ) >= 0:
            mQueue.addQueue( message.content.split(" ")[1] )

            # 新規再生
            if not vc.is_playing():
                
                mQueue.popQueue()
                src = nc.getVideo( mQueue.nowPlaying["url"] )
                time.sleep( 5 )
                vc.play( discord.FFmpegPCMAudio( src ) )
                vc.source = discord.PCMVolumeTransformer( vc.source )
                vc.source.volume = 0
                isPlay = True
                t1.start()         

        await message.channel.send( mQueue.now() )

    elif message.content == "#stop":

        # 一時停止
        vc.pause()
        await message.channel.send( "pause" )

    elif message.content == "#skip":
        
        await message.channel.send( "skip" )
        vc.stop()
        nc.isDownload = False
    
    elif message.content == "#queue":
        
        await message.channel.send( mQueue.showQueue() )

    elif message.content.startswith("#remove"):

        if int( message.content.split(" ")[1] ) >= 0:
            m = "remove {0}".format( mQueue.popQueue[ int( message.content.split(" ")[1]) ]["title"] )
            mQueue.removeQueue( int( message.content.split(" ")[1] ) )
            await message.channel.send( m )
        
        else:
            await message.channel.senf( "error invalid index" )

    elif message.content == "#now":
        await message.channel.send( "{0}\n{1}\n{2}\n{3}".format( vc.is_paused(), vc.timeout , vc.is_playing(),  mQueue.now() ) )

    elif message.content == "dc":
        await vc.disconnect()
        vc = None
        await message.channel.send("disconnect")        
        
client.run( myToken.discord_token )