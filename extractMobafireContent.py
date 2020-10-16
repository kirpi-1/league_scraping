import utils
from bs4 import SoupStrainer
import argparse

# if the purge flag is set to True, then purge all progress and start over from the beginning
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--purge', default = False, action = 'store_true')
args = parser.parse_args()
purge = args.purge

# site information
game = 'LeagueMobafire'
siteName = "mobafire"
baseurl = "https://www.mobafire.com/league-of-legends/"

# create strainers that get only website data whose tag has id="content"
content = SoupStrainer(id="content")
strainers = [content]


# remove data under these html tags
tagsToRemove = ['script', 'meta','style']

# remove data that has class equal to the following list
classesToRemove = ['collapsible', 'references', 'printfooter','comments','quick-comment','sidebar-module','mf-sort',
					'champ-pages__page champ-pages__page--current champ-pages__page--no-top-margin',
					'comments comments-main','user-level']

# actual call to get data
utils.mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, purge = purge)

