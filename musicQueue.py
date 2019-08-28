import nico2

class QueueCtrl( ):

    def __init__( self ):

        self.playQueue:list = list()
        self.notPlaying = { "title": None }
        self.nowPlaying = self.notPlaying
        self.nc = nico2.nico2py()

    def popQueue( self ):
        try:
            self.nowPlaying = self.playQueue.pop()
        except IndexError:
            self.nowPlaying = self.notPlaying

        return self.nowPlaying
        
    def addQueue( self, smUrl ):
        dic = self.nc.getInfo(smUrl)
        self.playQueue.append( self.nc.getInfo(smUrl) )
        return( dic["title"] )

    def removeQueue( self, index ):
        
        ret = self.playQueue[index]
        self.playQueue.remove( self.playQueue[index] )
        return ret

    def showQueue( self ):
        
        ql = "{0} : {1}\n".format( "now", self.nowPlaying["title"] )

        for i in range( len(self.playQueue) ):
            
            ql += "{0} : {1}\n".format( i, self.playQueue[i]["title"] )

        return ql

    def now( self ):
        
        m = "now `{0}`".format( self.nowPlaying["title"] )
        return m
