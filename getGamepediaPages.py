# -*- coding: utf-8 -*-
"""
Created on

@author: Zack Wisti
"""
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
for p in portals:
	print(baseurl+p)
	resp = requests.get(baseurl+p)
	strainer = SoupStrainer(class_=["tabheader-tab",'mw-body-content'])
	soup = BeautifulSoup(resp.content,'lxml',parse_only=strainer)
	l = list()
	soup.find('div', id="top-schedule").decompose()
	for t in soup.find_all("a"):
		if 'href' in t.attrs and "http" not in t['href'] and t['href'][0] != "#" and "action=edit" not in t['href']:
			link = t['href']
			if link[0]=='/':
				link = link[1:]
			l.append(link)

	for a in l:
		pageList.append(a)
	time.sleep(1)

pageList = list(set(pageList))
pageList.sort()
remove = ["Patch", "Portal:", "2018", "File:","Bjergsen","TSM","Echo_Fox","#","Template:"]
for r in remove:
	pageList = [p for p in pageList if r not in p]

utils.write_list(pageList, "data/gamepedia.txt")


'''
navStrainer = SoupStrainer(class_="mw-allpages-nav")
bodyStrainer = SoupStrainer(class_="mw-allpages-body")

page = "/Special:AllPages"

if os.path.exists(pageListFilename):
	with open(pageListFilename, 'rb') as f:
		f.seek(-2, os.SEEK_END)
		while f.read(1) != b'\n':
			f.seek(-2, os.SEEK_CUR)
		last_line = f.readline().decode()
		page = "/index.php?title=Special:AllPages&from="+last_line[1:].strip()
		print("starting at: ", baseurl+page)
		time.sleep(5)

while not page=="":
	#clear_output(wait = True)
	print("At page: {}".format(baseurl + page))
	req = requests.get(baseurl+page)
	nav  = BeautifulSoup(req.content, "lxml", parse_only=navStrainer)
	body = BeautifulSoup(req.content, "lxml", parse_only=bodyStrainer)

	# find the "next page" link and add it to the list


	pageList = list()
	for tag in body.find_all("a"):
		t = tag['href']
		if re.match("/",t):
			t = re.sub("/","",t,count=1)
		pageList.append(t)

	utils.append_to_file(pageList,pageListFilename)
	time.sleep(1)
	# get the "next page" link and request it
	# but only take the first one (there are at least 2 on the page)
	page = ""
	for tag in nav.find_all("a"):
		if "Next page" in tag.string:
			page = tag['href']
			curPageTitle = tag.string.replace("Next page","")
			break





'''
print("finished")
