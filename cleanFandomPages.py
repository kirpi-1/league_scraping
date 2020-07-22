# -*- coding: utf-8 -*-
"""
Created on 7/16/2020

@author: Zack Wisti, Stacie Sanchez
"""
import requests
import time
from bs4 import BeautifulSoup, SoupStrainer
import utils
import os
import re

badList = ['https://leagueoflegends.fandom.com/wiki/Category:LoL_patch_notes',
            'https://leagueoflegends.fandom.com/wiki/Category:LoL_patch_notes?from=V6.20',
            'https://leagueoflegends.fandom.com/wiki/Category:Contracted_artists',
            'https://leagueoflegends.fandom.com/wiki/Category:Riot_Games_staff',
            'https://leagueoflegends.fandom.com/wiki/Category:Riot_Games_staff?from=Justin+%27Earp%27+Albers',
            'https://leagueoflegends.fandom.com/wiki/Category:Events',
            'https://leagueoflegends.fandom.com/wiki/Category:Tournaments',
            'https://leagueoflegends.fandom.com/wiki/Category:WR_finished_items',
            'https://leagueoflegends.fandom.com/wiki/Category:Anniversary'
            ]

# Go through remove list
removeList = list()
for r in badList:
    print(r)
    resp = requests.get(r)
    strainer = SoupStrainer(class_=['category-page__member'])
    soup = BeautifulSoup(resp.content,'lxml',parse_only=strainer)
    l = list()
    #soup.find('div', id="top-schedule").decompose()
    for t in soup.find_all("a"):
        if 'href' in t.attrs and "http" not in t['href'] and "#" not in t['href'] and "action=edit" not in t['href']:
            link = t['href']
            # remove '/wiki/' from beginning of link
            link = link.replace("/wiki/","")
            l.append(link)

    for a in l:
        removeList.append(a)
    time.sleep(1)

removeList = list(set(removeList))
baseList = utils.load_list("data/LeagueFandom.txt")

# Go through every item in removeList and remove it from baseList
for w in removeList:
    baseList = [b for b in baseList if b!=w]

utils.write_list(baseList,'data/LeagueFandom.txt')
