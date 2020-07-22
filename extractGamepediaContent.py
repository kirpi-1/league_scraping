# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 20:34:17 2019

@author: Veronica Chu, Zack Wisti
"""
import utils
from bs4 import SoupStrainer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--purge', default = False, action = 'store_true')

args = parser.parse_args()
purge = args.purge
game = 'LeagueGamepedia'
siteName = "gamepedia"
baseurl = "https://lol.gamepedia.com/"

header = SoupStrainer(id="firstHeading")
body = SoupStrainer(id="bodyContent")

strainers = [header, body]
tagsToRemove = ['script', 'meta','style']
classesToRemove = ['references', 'tabheader-top','noprint','topschedule-header','topschedule-box']
utils.mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, purge = purge)
