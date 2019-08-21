import nico2

class musicPlayer():

    def __init__( self ):

        self.playQueue:list = list()
        self.notPlaying = { "title": None }
        self.nowPlaying = self.notPlaying
        self.nc = nico2.nico2py()

    def play( self ):
        try:
            self.nowPlaying = self.playQueue.pop()
        except IndexError:
            self.nowPlaying = self.notPlaying

        return self.nowPlaying
        
    def addQueue( self, smUrl ):
        self.playQueue.append( self.nc.getInfo(smUrl) )

    def removeQueue( self, index ):

        self.playQueue.remove( self.playQueue[index] )

    def showQueue( self ):
        
        ql = "{0} : {1}\n".format( "now", self.nowPlaying["title"] )

        for i in range( len(self.playQueue) ):
            
            ql += "{0} : {1}\n".format( i, self.playQueue[i]["title"] )

        return ql

    def now( self ):
        
        m = "now : {0}".format( self.nowPlaying["title"] )
        return m
