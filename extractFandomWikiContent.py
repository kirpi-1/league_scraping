import utils
from bs4 import SoupStrainer
import argparse

# if the purge flag is set to True, then purge all progress and start over from the beginning
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--purge', default = False, action = 'store_true')
args = parser.parse_args()
purge = args.purge

# site information
game = 'League'
siteName = "LeagueFandom"
baseurl = "https://leagueoflegends.fandom.com/wiki/"

# create strainers that get items of class="page-header__main" or "WikiaArticle"
headerStrain = SoupStrainer(class_="page-header__main")
pageStrain = SoupStrainer(class_="WikiaArticle")
strainers = [headerStrain, pageStrain]

# remove data under these html tags
tagsToRemove = ['script', 'meta','style']

# remove data that has class equal to the following list
classesToRemove = ['collapsible', 'references', 'printfooter','WikiaArticleFooter','edit-info-user','edited-by',
'va-collapsible-content mw-collapsible mw-made-collapsible mw-collapsed']

# actual call to get data
utils.mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, purge = purge)

