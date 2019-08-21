import discord
import myToken
import nico2

client = discord.Client()
nc = nico2.nico2py()
vc:discord.VoiceClient = None

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

    if message.content == "e":
        await client.logout()
    
    elif message.content.startswith("#play"):

        if nc.isDownload == True:
            await message.channel.send( "now playing! please skip" )
        
        else:

            if vc == None:
                vc = await message.author.voice.channel.connect()
                await message.channel.send( "connect!" )
            
            if vc.is_playing():
                pass
                
            else:
                l = message.content.split(" ")
            
                vc.play( discord.FFmpegPCMAudio(  nc.getVideo( l[1] ) ) )
                vc.source = discord.PCMVolumeTransformer( vc.source )
                vc.source.volume = 0.05

            await message.channel.send( "play" )

    elif message.content == "#stop":

        vc.stop()
        await message.channel.send( "stop" )

    elif message.content == "#skip":
        nc.isDownload = False
        vc.stop()
        await message.channel.send( "skip" )

    elif message.content == "dc":
        await vc.disconnect()
        vc = None
        await message.channel.send("disconnect")

client.run( myToken.discord_token )