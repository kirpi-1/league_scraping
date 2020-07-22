# -*- coding: utf-8 -*-
"""
Created on 4/18/20

@author: Zack Wisti
"""
import requests
import time
from bs4 import BeautifulSoup, SoupStrainer
import utils
import re

# get all pages from mobafire
sitemapurl = "https://www.mobafire.com/sitemap.xml"

page = requests.get(sitemapurl)
strainer = SoupStrainer("loc")
soup = BeautifulSoup(page.content,"lxml",parse_only=strainer)
sitemap = list()
for l in soup.find_all("loc"):
	sitemap.append(l.text)
visitedPages = []
pageList = []
while len(sitemap)>0:
	time.sleep(2)
	print("{} pages left".format(len(sitemap)))
	site = sitemap.pop(0)
	if not site in visitedPages:
		visitedPages.append(site)
		page = requests.get(site)
		soup = BeautifulSoup(page.content, 'lxml')
		text = re.split("\s+",soup.get_text())
		for t in text:
			if "http" in t:
				if t not in visitedPages:
					if ".xml" in t :
						sitemap.append(t)
					else:
						pageList.append(t)

remove = ['build', 'teamfight-tactics','stream','blog','video','tier-list','/wiki/mobafire','forum','news','toplist','tournaments']

refined = [p.replace("https://www.mobafire.com/league-of-legends/","") for p in pageList if "league-of-legends" in p]
for r in remove:
    refined = [item for item in refined if r not in item]

builds = [u +"/stats" for u in refined if "champion/" in u]
for b in builds:
	refined.append(b)

refined.sort()


utils.write_list(refined,"data/mobafire.txt")
