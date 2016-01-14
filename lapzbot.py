import discord
import urllib.request
import json
import requests
import bs4
import time
##import lxml.html

client = discord.Client()
client.login('Username', 'Password')

@client.event
def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('{} hello'.format(client.user.mention())):
        client.send_message(message.channel, 'Hello {}'.format(message.author.mention()))

    if message.content.startswith('{} help'.format(client.user.mention())):
        client.send_message(message.channel, 'Hello {}, the following commands are available:- `hello`, `help`, `stats <username>`, `top <username>`, `wtf`'.format(message.author.mention()) +'\n'+'For stats <username> and top <username> make sure to use _(underscore) if your username contains 2 words or more. Example:- `@lapzbot stats John_Smith`')

    if message.content.startswith('{} wtf'.format(client.user.mention())):
        client.send_message(message.channel, 'WTF!!! {}'.format(message.author.mention()))
## osu! API functions-----------------------------------------------------------------------------------
    if message.content.startswith('{} stats'.format(client.user.mention())):
        my_string = message.content    
        splitted = my_string.split()
        first = splitted[0]
        second = splitted[1]
        third = splitted[2]
## Rework the permissions later
##        allow = discord.Permissions.none()
##        deny = discord.Permissions.none()
##        #allow.can_mention_everyone = True
##        deny.can_embed_links = True
##        membs = discord.utils.find(lambda m: m == client.user, message.server.members)
##        client.set_channel_permissions(message.channel, membs, allow, deny)

        r=requests.get('https://osu.ppy.sh/api/get_user?k=API Key&u='+third)
        data=r.json()
        for player in data:
            client.send_message(message.channel,'https://a.ppy.sh/'+player['user_id'] + '\nUsername : ' + player['username'] + '\nPerformance Points : ' + "%.2f" % float(player['pp_raw']) +  '\nAccuracy : ' + "%.2f" % float(player['accuracy']) + '\nPlaycount : ' + player['playcount'] + '\nProfile Link : `osu.ppy.sh/u/'+player['user_id']+'`')

    if message.content.startswith('{} top'.format(client.user.mention())):
        my_string = message.content    
        splitted = my_string.split()
        first = splitted[0]
        second = splitted[1]
        third = splitted[2]
        

## Rework the permissions later       
##        allow = discord.Permissions.none()
##        deny = discord.Permissions.none()
##        #allow.can_mention_everyone = True
##        deny.can_embed_links = True
##        membs = discord.utils.find(lambda m: m == client.user, message.server.members)
##        client.set_channel_permissions(message.channel, membs, allow, deny)
        client.send_message(message.channel, 'Parsing the requested data. I may take some time. Please be patient.\n*Dont send me any other request before current request is completed, coz I am gonna ignore it.*\n\n')
        start_time = time.time()
        r = requests.get('https://osu.ppy.sh/api/get_user_best?k=API Key&u='+third+'&limit=5')
        data = r.json()
        msg = ''
        for player in data:
            thr = int(player['count300'])
            hun = int(player['count100'])
            fif = int(player['count50'])
            miss = int(player['countmiss'])
            tph = int(300*thr + 100*hun + 50*fif)
            tnh = int(thr + hun + fif + miss)
            acc = float(tph / (tnh*3))
            
            bitits = requests.get('https://osu.ppy.sh/b/'+player['beatmap_id'])
            html = bs4.BeautifulSoup(bitits.text, "lxml")
            tits = html.title.text

##            t = lxml.html.parse('https://osu.ppy.sh/b/'+player['beatmap_id'])
##            tits = t.find(".//title").text

           
            msg += str('Beatmap : ' + tits + ' `osu.ppy.sh/b/'+player['beatmap_id'] + '`' + '\n Acc : ' + "%.2f" % float(acc) + ' | ' + 'Rank : ' + player['rank'] + ' | ' + 'PP : ' + player['pp'] + '\n')

        client.send_message(message.channel, msg + '\nThis request took `'+ "%0.2s seconds`" % (time.time() - start_time)+' to process. Screw Peppy.')
        
## Chat Emotes--------------------------------------------------------------------------------------
    if message.content.startswith('!kappa'):
        client.send_message(message.channel, 'http://i.imgur.com/N5RzfBB.png')

    if message.content.startswith('!feelsbadman'):
        client.send_message(message.channel, 'http://i.imgur.com/DfURIfh.png')

    if message.content.startswith('!feelsgoodman'):
        client.send_message(message.channel, 'http://i.imgur.com/9Ggf2vs.png')

    if message.content.startswith('!lapz'):
        client.send_message(message.channel, 'http://i.imgur.com/I0Lqf3w.png')
        
@client.event
##def on_member_update(before, after):
##    bf_serv = before.server
##    af_serv = after.server
##    bf_status = before.status
##    af_status = after.status
##
##    if bf_status == 'offline' and af_status == 'online':
##        client.send_message(af_serv, 'Wassup {0}, welcome back !'.format(after.mention()))


@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
