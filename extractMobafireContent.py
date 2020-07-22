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


game = 'LeagueMobafire'
siteName = "mobafire"
baseurl = "https://www.mobafire.com/league-of-legends/"

content = SoupStrainer(id="content")

strainers = [content]
tagsToRemove = ['script', 'meta','style']
classesToRemove = ['collapsible', 'references', 'printfooter','comments','quick-comment','sidebar-module','mf-sort']
utils.mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, purge = purge)

