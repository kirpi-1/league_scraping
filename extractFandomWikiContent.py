# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 20:34:17 2019

@author: Veronica Chu, Zack Wisti
"""
import utils
import argparse
from bs4 import SoupStrainer

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--purge', default = False, action = 'store_true')

args = parser.parse_args()
purge = args.purge


game = 'League'
siteName = "LeagueFandom"
baseurl = "https://leagueoflegends.fandom.com/wiki/"

headerStrain = SoupStrainer(class_="page-header__main")
pageStrain = SoupStrainer(class_="WikiaArticle")

strainers = [headerStrain, pageStrain]
tagsToRemove = ['script', 'meta','style']
classesToRemove = ['collapsible', 'references', 'printfooter']
utils.mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, purge = purge)



'''

inProgressPagesFile = os.path.join("data","LeagueFandomInProgress.txt")
if os.path.exists(os.path.join("data","LeagueFandomInProgress.txt")):
	pageList = utils.load_list(inProgressPagesFile)
	print("found in-progress page list")	
else:
	print("loading original page list")
	pageList = load_list("data/LeagueFandom.txt")
	
time.sleep(1)
pagesVisitedFilename = os.path.join("data",game+"_PagesVistedList.txt")
urlsVisitedFilename = os.path.join("data",game + '_UrlsVistedList')
urlsVisited = []
if os.path.exists(urlsVisitedFilename):
	urlsVisited = util.load_list(urlsVisitedFilename)

failedPagesFilename = os.path.join("data",game + '_FailedPagesList')
redundantPagesFilename = os.path.join("data",game + '_RedundantPagesList')
completedPagesFilename = os.path.join("data",game + '_CompletedPagesList')
pagesToRemove = []
baseurl = 'https://leagueoflegends.fandom.com/wiki/'
folder = os.path.join("data",game+'Data')
#%% Collect majority of pages (based on having 'References' at end of page)
for idx, page in enumerate(pageList):	
	utils.printProgressBar(idx,len(pageList),"processing page {} of {}".format(idx+1,len(pageList)), length = 50)	#for console
	#update_progress(idx, len(pageList)) # for jupyter notebook
	
	try:		
		# keep track of pages already requested		
		utils.append_to_file(page, pagesVisitedFilename)		
		# get url
		url = baseurl + page		
		# before actually requesting the page, check if it's been visited before		
		if url in urlsVisited:
			redundantPages.append(page)
		else:
			# request the page
			soup = requests.get(url)
			# limit to 1 request every 2 seconds
			time.sleep(2)
			# get actual (redirected) url and generate filename from that
			actualurl = soup.url.split("#")[0]
			leaf = actualurl.split("wiki/")[-1]
			filename = "".join(re.split('\W+',leaf))+".txt"
			fullpath = os.path.join(folder,filename)
			# check if webpage has already been collected (e.g. redirects)
			#print("does {} exist?".format(fullpath),os.path.exists(fullpath))
			#print("visited {} before?".format(actualurl), actualurl in urlsVisited)
			
			if actualurl in urlsVisited:
				utils.append_to_file(page, redundantPagesFilename)
			else:
				# add to list of urls visted
				utils.append_to_file(actualurl, urlsVisitedFilename)
				urlsVisited.append(actualurl)
				
				# parse header
				headerStrain = SoupStrainer(class_="page-header__main")
				headerSoup = BeautifulSoup(soup.content, 'html.parser', parse_only=headerStrain)
				utils.remove_tag(headerSoup,'script')
				utils.remove_tag(headerSoup,'meta')
				utils.remove_tag(headerSoup,'style')
				headerText = headerSoup.get_text()
				
				# parse main article
				pageStrain = SoupStrainer(class_="WikiaArticle")
				pageSoup = BeautifulSoup(soup.content, 'html.parser', parse_only=pageStrain)
				
				utils.remove_class(pageSoup, "collapsible")
				utils.remove_class(pageSoup, "references")
				utils.remove_class(pageSoup, "printfooter")
				utils.remove_tag(pageSoup, 'script')
				utils.remove_tag(pageSoup, 'meta')
				utils.remove_tag(pageSoup, 'style')

				pageText = []
				for s in pageSoup.stripped_strings:
					pageText.append(s)

				# get titles from all links to other pages that don't have text
				links = pageSoup.find_all('a')
				linkText = []
				for idx, l in enumerate(links):	
					if 'title' in l.attrs.keys():
						if l.string==None:
							linkText.append(l['title'])


				fullText = " ".join([headerText, *pageText,*linkText])
				t = re.split("\W+",fullText)
				fullText = actualurl + "\n" + " ".join(t)

				# save content to text file				
				utils.save_textFile(str(fullText), fullpath)
				# add page to completed list
				utils.append_to_file(page, completedPagesFilename)

			# end if actualURL not in urlsVisited
		# end not os.path.exists(p) and url not in urlsVisited		
		# add page to list of files to remove
		pagesToRemove.append(page)
	except:
		e = sys.exc_info()		
		# keep track of pages that failed to get data from				
		utils.append_to_file(page, failedPagesFilename)		
		print("error!", e, "on",page)
		traceback.print_exc(file=sys.stdout)
		break

# remove pages we've gone through and write those to the in-progress list
if len(pagesToRemove)>0:
	for p in pagesToRemove:
		pageList.remove(p)
	utils.write_list(pageList,inProgressPagesFile)
	
'''

