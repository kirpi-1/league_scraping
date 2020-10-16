# Gets a page list from the League of Legends Gamepedia wiki
# Pages are selected from the "Portals" category, a type of page for game-specific information
# Gamepedia is mostly an E-Sports oriented website, so using this portal is necessary for excluding e-sports information
# It removes certain types of pages (such as template pages and those related to patch notes) and duplicate urls,
# then formats the pages to be used during extraction

import requests
import time
from bs4 import BeautifulSoup, SoupStrainer
import utils
import os
import re

#%%
site = 'gamepedia'

pageListFilename = "data/gamepedia.txt"

portals = ['/New_To_League/Welcome',
		   '/Portal:Champions',
		   '/Portal:Items',
		   '/Portal:Minions',
		   '/Portal:Monsters',
		   '/Portal:Summoner_Spells',
		   '/Portal:Runes',
		   '/Portal:Patch_Notes',
		   '/Portal:Game_Modes',
		   '/Portal:Miscellaneous']

baseurl = "https://lol.gamepedia.com"
pageList = list()
# for each portal, scan for links in the main body of the page
for p in portals:
	print(baseurl+p)
	resp = requests.get(baseurl+p)
	strainer = SoupStrainer(class_=["tabheader-tab",'mw-body-content'])
	soup = BeautifulSoup(resp.content,'lxml',parse_only=strainer)
	l = list()
	soup.find('div', id="top-schedule").decompose()
	# find all "a" tags, then grab only the ones that have a link (i.e. 'href')
	for t in soup.find_all("a"):
		if 'href' in t.attrs and "http" not in t['href'] and t['href'][0] != "#" and "action=edit" not in t['href']:
			link = t['href']
			if link[0]=='/':
				link = link[1:]
			l.append(link)
	# add to the list of links
	for a in l:
		pageList.append(a)
	time.sleep(1)

pageList = list(set(pageList))
pageList.sort()
remove = ["Patch", "Portal:", "2018", "File:","Bjergsen","TSM","Echo_Fox","#","Template:"]
for r in remove:
	pageList = [p for p in pageList if r not in p]

utils.write_list(pageList, "data/gamepedia.txt")

print("finished")
