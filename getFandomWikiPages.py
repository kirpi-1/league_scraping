# Gets a page list from the League of Legends Fandom wiki
# This uses the wiki function, "Special:AllPages" to get a list of every page in the wiki
# Finally, it removes duplicate urls and formats the pages to be used during extraction

import requests
import time
from bs4 import BeautifulSoup, SoupStrainer
import utils
import re

game = 'League'
url = 'https://leagueoflegends.fandom.com/wiki/Special:AllPages'
baseurl = 'https://leagueoflegends.fandom.com'

#%% Table of sections of all page list
# Get links to sections of all pages list to comb through for page links

# request page with target data
page = requests.get(url)

# filter the HTML content for the sections of page lists
allpagesStrain = SoupStrainer(class_="allpageslist")
allpagesSoup = BeautifulSoup(page.content, 'html.parser', parse_only=allpagesStrain)

allpagesList = []
# add page directories to a list
for link in allpagesSoup.find_all('a'):
    linkString = link.get('href')    
    allpagesList.append(linkString)
allpagesList = mylist = list(dict.fromkeys(allpagesList))

#%% Comb through the sections of the all page list to collect the pages
pageList = []
utils.printProgressBar(0,len(allpagesList),"parsing {} of {}".format(0, len(allpagesList)))
for idx,link in enumerate(allpagesList):    
    utils.printProgressBar(idx,len(allpagesList),"parsing {} of {}".format(idx+1, len(allpagesList)))
	# request page
    url = baseurl + link
    page = requests.get(url)
    
    # filter for table content
    pageStrain = SoupStrainer(class_="mw-allpages-table-chunk")
    pagesSoup = BeautifulSoup(page.content, 'html.parser', parse_only=pageStrain)
    
    # add the pages to a list
    for link in pagesSoup.find_all('a'):
        linkString = link.get('href')
        if not "Legends_of_Runeterra" in linkString:
            pageList.append(linkString)    
    time.sleep(2)
utils.printProgressBar(idx,len(allpagesList),"parsing {} of {}".format(len(allpagesList), len(allpagesList)))

#%% Clean page list

# 1 - remove duplicates while maintaining alphabetical order of page titles
pageList = list(dict.fromkeys(pageList))

# 2- remove parent pages of children pages to prevent duplicates
# remove '/wiki/'
cleanpageList = []
for item in pageList:
    temp = item.split('/wiki/')
    cleanpageList.append(temp[1])

# get parent pages
parentPages = []
for item in cleanpageList:
    if '/' in item:
        temp = item.split('/')
        parentPages.append(temp[0])
parentPages = list(set(parentPages))

# remove parent pages from page list and sort alphabetically
cleanpageList = list(set(cleanpageList) - set(parentPages))
cleanpageList.sort()

cleanpageList = [b for b in cleanpageList if "Teamfight_Tactics" not in b]
cleanpageList = [b for b in cleanpageList if "Wild_Rift" not in b]
cleanpageList = [b for b in cleanpageList if re.match("[vV][\d*\.]+",b)==None]

# save list
#utils.save_pickleObject(cleanpageList, str(game + 'PageList'))
filename = "data/LeagueFandom.txt"
with open(filename,'w') as f:
    for l in cleanpageList:
        f.write(str(l)+'\n')
