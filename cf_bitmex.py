#!/usr/bin/python3

from twitter import *
from email.utils import parsedate
import ts3
import time
import datetime
from telegram import *
import telegram


def is_number(s):
   try:
        int(s)
        return True
   except:
        return False
 
def addcommas(string):
    words=string.split()
    newcall=""
    for word in words:
        if is_number(word) == True:
            word2="{:,}".format(int(word))
            newcall = newcall + " " + word2
        else:
            newcall = newcall + " " + word
    return str(newcall[1:])


t = Twitter(auth=OAuth('xxxxxxxxxx', 'zzzzzzzzz', 'yyyyyyyyy', 'vvvvvvvvvv'))

# fetch last update id from external file
f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastaltmexupdate.txt', encoding='utf-8')
latestid = f.readline().strip()
f.close()

if (latestid == ""):
	latestid=1

# grab tl updates
updates=timeline=t.statuses.user_timeline(screen_name="bitmexrekt", count=30)
wclist=list()
#loop through updates
for update in reversed(updates):
	text = update['text']
	tweetid = str(update['id'])
	print(tweetid)
	if (int(latestid) < int(tweetid)):
		timestamp = update['created_at']
		wclist.append(text)
		latestid=tweetid
		f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastaltmexupdate.txt', '+w', encoding='utf-8')
		f.write(latestid)
		f.close()


if not wclist:
	f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastaltmexupdate.txt', 'w+', encoding='utf-8')
	f.write(str(latestid))
	f.close()

else:
	with ts3.query.TS3Connection("158.69.115.146", 2009) as ts3conn:
		try:
			ts3conn.login(
			client_login_name="xxxxxx",
			client_login_password="zzzzzzzzzz"
			)
		except ts3.query.TS3QueryError as err:
			print("Login failed:", err.resp.error["msg"])
			exit(1)
		ts3conn.use(sid=778)
		ts3conn.clientupdate(client_nickname="[CoinFarm]")
		#token='153606345:AAGDdKnw41oLce5axJfKlqutMEnnb5jfnAQ'
		#bot=telegram.Bot(token=token)
		resp = ts3conn.whoami()
		client_id=resp[0]['client_id']
		ts3conn.clientmove(cid=44184, clid=client_id)
		for s in wclist:
			if 'XBT' in s:
				continue
			#ts3conn.sendtextmessage(targetmode=2, target=1, msg=s)
			ts3conn.sendtextmessage(targetmode=2, target=1, msg="[url=http://bitmex.whalepool.io]BitMEX[/url]: "+s)
			#ts3conn.clientmove(cid=56600, clid=client_id)


		ts3conn.quit()

f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastaltmexupdate.txt', '+w', encoding='utf-8')
f.write(latestid)
f.close()
