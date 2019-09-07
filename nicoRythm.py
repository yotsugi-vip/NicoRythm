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
    
        if m_content.startswith("#pl") or m_content.startswith("#playlist"):
            res.addQueue_playlist( m_content.split(" ")[1], vc )
            return

        await message.channel.send( res.player_play( vc, m_content ) )

    elif m_content == "#stop":
        await message.channel.send( res.player_stop( vc ) )

    elif m_content == "#skip" or m_content == "#s":
        await message.channel.send( res.player_skip(vc) )
    
    elif m_content == "#queue" or m_content == "#q":
        await message.channel.send( embed=res.player_queue() )

    elif m_content.startswith("#m"):
        res.moveQueue(m_content)

    elif m_content.startswith("#r"):
        await message.channel.send( res.player_remove( vc, message.content ) )

    elif m_content == "#now" or m_content == "#n":
        await message.channel.send( embed=res.player_now() )

    elif m_content.startswith("#addlist") or m_content.startswith("#al"):
        try:
            data:list = m_content.split(" ")
            await message.channel.send( res.add_playlist( data[1], data[2] ) )
        except IndexError:
            pass

    elif m_content.startswith("#showlist") or m_content.startswith("#sl"):
        await message.channel.send( embed=res.show_Queue( m_content.split(" ")[1] ) )

    elif m_content == "dc":
        await vc.disconnect()
        await message.channel.send("disconnect")        
        vc = None
        
    if m_content == "e":
        await client.logout()

    if m_content == "t":
        emb = discord.embeds.Embed()
        emb.description="description"
        emb.add_field( name="`Now`", value="[ぬきたし2 ED 「非実在系のわたし達」](https://www.nicovideo.jp/watch/sm35506385)", inline=True )
        emb.add_field( name = "`Lists`", value="`1`[【迷い猫オーバーラン！】はっぴぃ にゅう にゃあTVサイズ](https://www.nicovideo.jp/watch/sm25247794)\n`2`[ぬきたし2 ED 「非実在系のわたし達」](https://www.nicovideo.jp/watch/sm35506385)" )
        await message.channel.send(embed = res.show_Queue("nico"))




client.run( myToken.discord_token )
