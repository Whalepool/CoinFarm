#!/usr/bin/python3

import ts3
import datetime
from urllib.request import urlopen
import json
import math
import time
from twitter import *
import telegram
from num2words import num2words

url = "https://poloniex.com/public?command=returnTicker"
page = urlopen(url)
data=page.read()
decodedata=json.loads(data.decode())
lastprice=round(float(decodedata['BTC_REP']['last']),6)
f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastrep.txt', encoding='utf-8')
priorprice = f.readline().strip()
f.close()

f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastrep.txt', 'w+', encoding='utf-8')
f.write(str(lastprice))
f.close()

ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
pricediff = round(float(lastprice) - float(priorprice),6)
pricediff2 = abs(pricediff)
pricedifffrac = abs(pricediff) / float(priorprice)
pricediffperc = str(round(pricedifffrac*100,2))
f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/repfomologs.txt', 'a', encoding='utf-8')
f.write(str(ts) + " - " + str(lastprice) + " - " + pricediffperc + "\n")
f.close()
if pricediff < 0:
	direction = "down"
else:
	direction = "up"
if pricedifffrac > 0.01: 
	#fomotg = "ALERT: CLASSY is FOMO'ing " + direction + " by " + str(pricediff2) + " BTC (" + pricediffperc + "%) to " + str(lastprice) + " BTC in the past 5 minutes"
	#token='245046611:AAGddWcuQj4sWkbE2vvLeZiBwNw60Ja3ZlE'
	#bot=telegram.Bot(token=token)
	#bot.sendMessage(chat_id="@ethclassic", text=fomotg)

	f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/repfomologs.txt', 'a', encoding='utf-8')
	f.write(str(ts) + " - " + str(lastprice) + "ALERT: Augur REP is FOMO'ing [b]" + direction + "[/b] by " + pricediffperc + "% to [b] in the past 5 minutes\n")
	f.close()
	time.sleep(3)
	with ts3.query.TS3Connection("158.69.115.146", 2009) as ts3conn:
		try:
			ts3conn.login(
			client_login_name="xxxxxx",
			client_login_password="zzzzzzzz"
			)
		except ts3.query.TS3QueryError as err:
			print("Login failed:", err.resp.error["msg"])
			exit(1)
			#print(whalecallsupdate)
		ts3conn.use(sid=778)
		ts3conn.clientupdate(client_nickname="[CoinFarm]")
		#ts3conn.clientgetids(cluid="aS/5fz/mt08I1cY+UUvoALi7xOU=")
		#botid=ts3conn.last_resp.parsed[0]['clid']
	
		if "down" in direction:
			fomots = "ALERT: [color=red][b]Augur REP[/b][/color] is FOMO'ing [color=red][b]" + direction + "[/b][/color] by [color=red][b]" + str(pricediff2) + " BTC[/b][/color](" + pricediffperc + "%) to [color=red][b]" + str(lastprice) + " BTC[/b][/color] in the past 5 minutes"
		if "up" in direction:
			fomots = "ALERT: [color=green][b]Augur REP[/b][/color] is FOMO'ing [color=green][b]" + direction + "[/b][/color] by [color=green][b]" + str(pricediff2) + " BTC[/b][/color](" + pricediffperc + "%) to [color=green][b]" + str(lastprice) + " BTC[/b][/color] in the past 5 minutes"
		ts3conn.sendtextmessage(targetmode=2, target=1, msg=fomots)
		time.sleep(3)	
		resp = ts3conn.whoami()
		client_id=resp[0]['client_id']
		ts3conn.clientmove(cid=64382, clid=client_id)
		ts3conn.sendtextmessage(targetmode=2, target=1, msg=fomots)		
		#ts3conn.sendtextmessage(targetmode=1, target=botid, msg="!say \"CHOY-NAH is foe-mowing " + direction + " by " + str(num2words(float(pricediffperc))) + " percent. Check your PNL\"")		
		ts3conn.quit()
		
