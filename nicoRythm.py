import time
import discord
import myToken
import response as res

client = discord.Client()
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
    m_content = message.content

    if m_content.startswith("#p"):
        # 接続処理
        if vc == None:
            vc = await message.author.voice.channel.connect()
            await message.channel.send( "connect!" )
    
        await message.channel.send( res.player_play( vc, m_content ) )

    elif m_content == "#stop":
        await message.channel.send( res.player_stop( vc ) )

    elif m_content == "#skip" or m_content == "#s":
        await message.channel.send( res.player_skip(vc) )
    
    elif m_content == "#queue" or m_content == "#q":
        await message.channel.send( res.player_queue() )

    elif m_content.startswith("#r"):
        await message.channel.send( res.player_remove( vc, message.content ) )

    elif m_content == "#now" or m_content == "#n":
        await message.channel.send( res.player_now( vc ) )

    elif m_content == "dc":
        await vc.disconnect()
        await message.channel.send("disconnect")        
        vc = None
        
    if m_content == "e":
        await client.logout()

client.run( myToken.discord_token )