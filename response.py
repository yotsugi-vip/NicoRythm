import datetime
import json
import math
import os
import threading
import time

import discord

import musicQueue
import nico2

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
                if mQueue.popQueue() != mQueue.notPlaying:
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

            if mQueue.popQueue() == mQueue.notPlaying:
                return
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

def player_now( ):
    global mQueue
    emb = discord.Embed()
    now = mQueue.now()
    emb.add_field( name="**Now Playing**", value="[{0}]({1})\n`{2}分{3}秒`"\
        .format( now["title"], now["url"], math.floor(now["duration"]/60), now["duration"]%60 ) )
    emb.set_thumbnail( url=now["thum"] )
    return emb

def player_queue( ):
    return mQueue.showQueue()

def add_playlist( listname:str, musicData:str ):
    global nc
    playlist = None

    if listname == None:
        return "no name"
    else:
        listname = "playlists/{0}.json".format( listname )

    if os.path.exists( listname ):
        with open( listname, "r" ) as fp:
            playlist = json.load(fp)
    else:
        with open( "playlists/emptylist.json", "r" ) as fp:
            playlist = json.load(fp)
        
    playlist["playlist"].append( nc.getInfo( musicData ) )

    with open(listname,"w") as fp:
        json.dump( playlist, fp, indent=4 )
    return "Queue Added"
    
def addQueue_playlist( listname:str, vc:discord.VoiceClient ):
    global mQueue
    playlist = None

    if not os.path.exists( "playlists/{0}.json".format(listname) ):
        return "Err list not exists"

    else:
        with open( "playlists/{0}.json".format(listname), "r") as fp:
            playlist = json.load(fp)

        for i in range( len(playlist["playlist"]) ):
            if i == 0:
                player_play( vc, " {0}".format( playlist["playlist"][i]["url"] ) )
            else:
                mQueue.playQueue.append( playlist["playlist"][i] )

def show_Queue( listname:str ):
    playlist = None
    emb = discord.Embed()
    index = 0
    duration = 0
    ql = str()

    if not os.path.exists( "playlists/{0}.json".format(listname) ):
        return "Err list not exists"

    else:
        with open( "playlists/{0}.json".format(listname), "r") as fp:
            playlist = json.load(fp)
            for item in playlist["playlist"]:
                ql += "`{0}.`[{1}]({2})|`{3}分{4}秒`\n\n".format( index, item["title"], item["url"], math.floor(item["duration"]/60), item["duration"]%60 )
                index += 1
                duration += item["duration"]
            ql += "合計{0}曲\n再生時間:`{1}分{2}秒`".format( index, math.floor(duration/60), duration%60 )
            emb.add_field( name="**List {0}**".format(listname), value=ql )
        return emb

def moveQueue( m ):
    try:
        global mQueue
        a = int( m.split()[1] )
        b = int( m.split()[2] )
        mQueue.playQueue[a], mQueue.playQueue[b] = mQueue.playQueue[b], mQueue.playQueue[a]
        ret = True
    except:
        ret = False
    finally:
        return ret

def showHelp():
    emb = discord.Embed()
    emb.add_field(name="`#play [url]` `#p [url]`", value="urlの動画を再生\n一時停止時はレジューム",inline=False)
    emb.add_field(name="`#stop`",value="音声を一時停止する", inline=False)
    emb.add_field(name="`#skip` `#s`", value="次の曲を再生", inline=False)
    emb.add_field(name="`#queue` `#q`", value="現在のキューを確認", inline=False)
    emb.add_field(name="`#move [index] [index]` `#m [index] [index]`", value="キューの順番を入れ替える",inline=False)
    emb.add_field(name="`#remove [index]`",value="該当キューを削除",inline=False)
    emb.add_field(name="`#now` `#n`", value="現在の再生曲情報",inline=False)
    emb.add_field(name="`#addlist [listname] [url]` `#al [listname] [url]`",value="プレイリストに曲を追加する",inline=False)
    emb.add_field(name="`#showlist [listname]` `#sl [listname]`", value="プレイリストの内容を表示",inline=False)
    emb.add_field(name="`#disconnect` `#dc`", value="ボイスから切断する",inline=False)
    emb.title = "**COMMANDS**"
    return emb
