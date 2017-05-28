#!/usr/bin/python3

import ts3
import datetime
from urllib.request import urlopen
import json
import math
import time

# Whalepool Shitcoin Index (WSI)
# Index of top 10 shitcoins by marketcap
# 1000 pts = standardized to 1 Billion USD
# Uses CoinMarketCap to determine rank and marketcap (by USD)

#scrape from coinmarketcap
url = "https://api.coinmarketcap.com/v1/ticker/?limit=15"

#grab url
page = urlopen(url)

#read data
data=page.read()

nonrankcoins=['PIVX', 'USDT']

#load json to grab coin parms
wsi=json.loads(data.decode())
marketcaptotal=0
menrank=0
#sum the marketcaps
for x in range(1,11):
	if wsi[x]['symbol'] in nonrankcoins:
		continue
	menrank=menrank+1;
	if menrank>10:
		break
	print(float(wsi[x]['market_cap_usd']))
	marketcaptotal=float(marketcaptotal)+float(wsi[x]['market_cap_usd'])
	
marketcaptotal=round(marketcaptotal,0)
print(marketcaptotal)
#WSI is just marketcap standardized to 1 billion to 1000 pts
wsivalue=(marketcaptotal/1000000000)*1000

#f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/wsidata1.txt', 'a', encoding='utf-8')
#f.write(str(round(time.time())) + "," + str(round(wsivalue,2)))
#f.write("\n")
#f.close()

#grab poloniex ticker for BTC 24Hr pct change

url2= "https://poloniex.com/public?command=returnTicker"
#grab url
page2 = urlopen(url2)

#read data
data2=page2.read()

#load json to grab coin parms
poloticker=json.loads(data2.decode())


weightedpct=0
minrank=0
for x in range(1,15):
	if wsi[x]['symbol'] in nonrankcoins:
		continue
	minrank=minrank+1;
	if minrank>10:
		break
	weightedpct=weightedpct+(float(wsi[x]['percent_change_24h'])*(float(wsi[x]['market_cap_usd'])/marketcaptotal))

#build individual message

if weightedpct<0 :
	if weightedpct<-1:
		indexcomponentsmsg="[1-HOUR WSI10 Ticker]: [b][color=red]" + str(round(wsivalue,2)) + " (" + str(round(weightedpct,2)) + "%)[/color][/b] [u]24H Change[/u]. Top 10 by MarketCap: "
	else:
		indexcomponentsmsg="[1-HOUR WSI10 Ticker]: [color=red]" + str(round(wsivalue,2)) + " (" + str(round(weightedpct,2)) + "%)[/color] [u]24H Change[/u]. Top 10 by MarketCap: "
else:
	if weightedpct>1:
		indexcomponentsmsg="[1-HOUR WSI10 Ticker]: [b][color=green]" + str(round(wsivalue,2)) + " (+" + str(round(weightedpct,2)) + "%)[/color][/b] [u]24H Change[/u]. Top 10 by MarketCap: "
	else:
		indexcomponentsmsg="[1-HOUR WSI10 Ticker]: [color=green]" + str(round(wsivalue,2)) + " (+" + str(round(weightedpct,2)) + "%)[/color] [u]24H Change[/u]. Top 10 by MarketCap: "

muhrank=0

for x in range(1,15):
	if wsi[x]['symbol'] in nonrankcoins:
		continue
	muhrank=muhrank+1;
	if muhrank>10:
		break
	poloprice=round((float(poloticker['BTC_' + wsi[x]['symbol']]['percentChange']))*100,2)
	#print(poloprice)
#str(wsi[x]['percent_change_24h'])
	if poloprice<0:
		if poloprice<-5:
			indexcomponentsmsg=indexcomponentsmsg + str(muhrank) + ". [b][color=red]" + wsi[x]['name'] + " (" + wsi[x]['symbol'] + "): " + wsi[x]['price_btc'] + " BTC (" + str(poloprice) + "%),[/color][/b] "
		else:
			indexcomponentsmsg=indexcomponentsmsg + str(muhrank) + ". [color=red]" + wsi[x]['name'] + " (" + wsi[x]['symbol'] + "): " + wsi[x]['price_btc'] + " BTC (" + str(poloprice) + "%),[/color] "
	else:
		if poloprice>5:
			indexcomponentsmsg=indexcomponentsmsg + str(muhrank) + ". [b][color=green]" + wsi[x]['name'] + " (" + wsi[x]['symbol'] + "): " + wsi[x]['price_btc'] + " BTC (+" + str(poloprice) + "%), [/color][/b]"
		else:
			indexcomponentsmsg=indexcomponentsmsg + str(muhrank) + ". [color=red]" + wsi[x]['name'] + " (" + wsi[x]['symbol'] + "): " + wsi[x]['price_btc'] + " BTC (" + str(poloprice) + "%),[/color] "
		
print(indexcomponentsmsg)
with ts3.query.TS3Connection("158.69.115.146", 2009) as ts3conn:
        try:
                ts3conn.login(
                        client_login_name="xxxxxxx",
                        client_login_password="zzzzzzzz"
                )
        except ts3.query.TS3QueryError as err:
                print("Login failed:", err.resp.error["msg"])
                exit(1)

        ts3conn.use(sid=778)
        ts3conn.clientupdate(client_nickname="[CoinFarm]")
        resp = ts3conn.whoami()
        client_id=resp[0]['client_id']
        ts3conn.clientmove(cid=64382, clid=client_id)
        ts3conn.sendtextmessage(targetmode=2, target=1, msg=indexcomponentsmsg)
        ts3conn.quit()

