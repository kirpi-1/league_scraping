import utils
from bs4 import SoupStrainer
import argparse

# if the purge flag is set to True, then purge all progress and start over from the beginning
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--purge', default = False, action = 'store_true')
args = parser.parse_args()
purge = args.purge

# site information
game = 'LeagueGamepedia'
siteName = "gamepedia"
baseurl = "https://lol.gamepedia.com/"

# create strainers that get data with id="firstHeading" or "bodyContent"
header = SoupStrainer(id="firstHeading")
body = SoupStrainer(id="bodyContent")
strainers = [header, body]

# remove data under these html tags
tagsToRemove = ['script', 'meta','style']

# remove data that has class equal to the following list
classesToRemove = ['references', 'tabheader-top','noprint','topschedule-header','topschedule-box','mw-collapsible']

# actual call to get data
utils.mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, purge = purge)
