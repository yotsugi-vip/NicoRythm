import math

import discord

import nico2


class QueueCtrl( ):

    def __init__( self ):

        self.playQueue:list = list()
        self.notPlaying = { "title": None }
        self.nowPlaying = self.notPlaying
        self.nc = nico2.nico2py()

    def popQueue( self ):
        try:
            self.nowPlaying = self.playQueue.pop( 0 )
        except IndexError:
            self.nowPlaying = self.notPlaying

        return self.nowPlaying
        
    def addQueue( self, smUrl ):
        try:
            dic = self.nc.getInfo(smUrl)
            self.playQueue.append( self.nc.getInfo(smUrl) )
            return( dic["title"] )
        except:
            return self.notPlaying

    def removeQueue( self, index ):
        try:
            ret = self.playQueue[index]
            self.playQueue.remove( self.playQueue[index] )
            return ret
        except:
            ret = self.notPlaying

    def showQueue( self ):
        emb = discord.Embed()
        ql = str()
        duration = 0
        i = 0

        try:
            emb.add_field( name="**Now Playing**", value="[{0}]({1})|`{2}分{3}秒`\n\n"\
            .format( self.nowPlaying["title"], self.nowPlaying["url"], math.floor(self.nowPlaying["duration"]/60), self.nowPlaying["duration"]%60 ) )

            emb.set_thumbnail(url=self.nowPlaying["thum"])
            duration += self.nowPlaying["duration"]
            
            for i in range( len(self.playQueue) ):
                
                ql += "`{0}.` [{1}]({2})|`{3}分{4}秒`\n\n"\
                .format( i, self.playQueue[i]["title"], self.playQueue[i]["url"], math.floor( self.playQueue[i]["duration"]/60 ), self.playQueue[i]["duration"]%60  )
                duration += self.playQueue[i]["duration"]

            ql += "`合計{0}曲`\n`再生時間{1}分{2}秒`".format( i+2, math.floor(duration/60), duration%60 )
            emb.add_field(name="**Queue**", value=ql)
        except:
            emb.add_field(name="**Not Playing**", value="----------------------")
        finally:
            return emb

    def now( self ):
        
        return self.nowPlaying
