import discord
import musicQueue
import time
import nico2
import threading
import os

isPlay = False
mQueue = musicQueue.QueueCtrl()
nc = nico2.nico2py()

def playcheck( vc:discord.VoiceClient, dummy ):
    global isPlay
    global nc
    global mQueue

    if isPlay:
        print("start")

    while isPlay:
        if vc.is_paused()  == False:
            time.sleep(0.5)
            if vc.is_playing() == False:
                mQueue.popQueue()
                src = nc.getVideo( mQueue.nowPlaying["url"] )
                while os.path.getsize(src) < 128:
                    pass

                vc.play( discord.FFmpegPCMAudio( src ) )
                vc.source = discord.PCMVolumeTransformer( vc.source )
                vc.source.volume = 0.1
                isPlay = True

def player_play( vc:discord.VoiceClient, m:str ):

    global nc
    global mQueue
    global isPlay

    ret = ""

    if m == "#play" or m == "#p":

        # 再開
        if vc.is_paused():
            vc.resume()
            ret = "Resuming!"

    # キュー追加
    elif m.find( "https://www.nicovideo.jp/watch/" ) >= 0:
        
        ret = "add `{0}`".format( mQueue.addQueue( m.split(" ")[1] ) )

        # 新規再生
        if not vc.is_playing():
            mQueue.popQueue()
            src = nc.getVideo( mQueue.nowPlaying["url"] )
            
            while os.path.getsize(src) < 256:
                pass

            vc.play( discord.FFmpegPCMAudio( src ) )
            vc.source = discord.PCMVolumeTransformer( vc.source )
            vc.source.volume = 0.1

            if not isPlay:
                isPlay = True
                t1 = threading.Thread( target=playcheck, args=( vc, 0 ) )
                t1.start()

            ret = "Play {0}".format( mQueue.now() )
        
    return ret

def player_stop( vc:discord.VoiceClient ):
    vc.pause()
    return "pause"

def player_skip( vc:discord.VoiceClient ):
    global nc

    vc.stop()
    nc.isDownload = False
    return "skip"

def player_remove( vc:discord.VoiceClient, m:str ):
    ret = ""
    if int( m.split(" ")[1] ) >= 0:
        res = mQueue.removeQueue( int( m.split(" ")[1] ) )
        ret = "remove{0}".format( res["title"] )
    else:
        ret = "Error invalid index"
    
    return ret

def player_now( vc:discord.VoiceClient ):
    global mQueue
    return mQueue.now()

def player_queue( ):
    return mQueue.showQueue()