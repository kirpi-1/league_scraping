# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 20:35:57 2019

@author: Veronica Chu, Zack Wisti
"""
#%%
import pickle

import requests, time, sys, os, bs4, traceback, re
from bs4 import BeautifulSoup, SoupStrainer


# save pickle object
def save_pickleObject(obj, name ):
	with open('data/'+ name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# load pickle object
def load_pickleObject(name ):
	with open('data/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)

# save a text file
def save_textFile(obj, path):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "w", encoding='utf-8', errors='ignore') as f:
		f.write(obj)
# load a text file
def load_textFile(name):
	mytext=[]
	with open('data/' + name, 'r', encoding='utf-8', errors='ignore') as f:
		mytext = f.read()

	return mytext

def write_list(l, filename):
	filename = add_txt_ext(filename)
	if os.path.dirname(filename)!='':
		os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename,'w',encoding='utf-8',errors='ignore') as f:
		for item in l:
			f.write(str(item)+'\n')

def load_list(filename):
	out = []
	with open(filename,'r', encoding='utf-8', errors ='ignore') as f:
		l = f.readline()
		while l!="":
			l = l.strip()
			out.append(l)
			l = f.readline()
	return out

def append_to_file(val, filename):
	filename = add_txt_ext(filename)
	if os.path.dirname(filename)!='':
		os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'a',encoding='utf-8',errors='ignore') as f:
		if type(val)==type(list()):
			for v in val:
				f.write(str(v)+"\n")
		else:
			f.write(str(val)+"\n")

def add_txt_ext(filename):
	path,ext = os.path.splitext(filename)
	if ext != "txt":
		filename = path+".txt"
	return filename

def remove_class(soup, class_):
	found = True
	while found:
		found = remove_class_h(soup, class_)

def remove_class_h(soup, class_):

	for desc in soup.descendants:
		if type(desc) == bs4.element.Tag and 'class' in desc.attrs.keys():
			for c in desc['class']:
				if class_ in c:
					desc.decompose()
					return True
	return False

def remove_tag(soup, tag):
	for script in soup([tag]):
		script.decompose()

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total	   - Required  : total iterations (Int)
		prefix	  - Optional  : prefix string (Str)
		suffix	  - Optional  : suffix string (Str)
		decimals	- Optional  : positive number of decimals in percent complete (Int)
		length	  - Optional  : character length of bar (Int)
		fill		- Optional  : bar fill character (Str)
		printEnd	- Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
	# Print New Line on Complete
	if iteration == total:
		print()

def getMobaAjaxHover(page):
	# for hover text
	soup = BeautifulSoup(page.content,'lxml')
	tags = soup.find_all(class_=['ajax-tooltip','tooltip-ajax'])
	tmp_text = list()

	for idx, tag in enumerate(tags):
		printProgressBar(idx+1,len(tags),length = 30, prefix="\t")#for console
		ajax_string = None
		for c in tag['class']:
			if re.search(".*t:.*i:.*",c)!=None: # find the one that is like '{t:ReforgedRune,i:61}'
				ajax_string = c
				break
		if ajax_string == None:
			continue
		tmp = ajax_string.split(',')[0]#t:ReforgedRune
		t = tmp[tmp.find("t:")+2:tmp.find(",")].replace("'","")
		tmp = ajax_string.split(',')[1]#61
		i = c[c.find("i:")+2:c.find("}")].replace("'","")
		if t != "SkinDetails":
			cURL=f"https://www.mobafire.com/ajax/tooltip?relation_type={t}&relation_id={i}"
			#print(cURL)
			indRunePage = requests.get(cURL)
			indRuneSoup = BeautifulSoup(indRunePage.content,'lxml')
			tmp_text.append(indRuneSoup.text.strip().replace('\n',' '))
	# end for tag in tags
	hover_text = " ".join(tmp_text)
	return hover_text

LeagueFandomBadCategories = ['LoL_patch_notes','Contracted_artists','Riot_Games_staff',
            'Events','Tournaments','WR_finished_items','Anniversary']

def mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, parser='lxml',purge=False):
	pagesVisitedFilename = os.path.join("data",siteName+"_PagesVisitedList.txt")
	urlsVisitedFilename = os.path.join("data",siteName + '_UrlsVisitedList.txt')
	failedPagesFilename = os.path.join("data",siteName + '_FailedPagesList.txt')
	redundantPagesFilename = os.path.join("data",siteName + '_RedundantPagesList.txt')
	completedPagesFilename = os.path.join("data",siteName + '_CompletedPagesList.txt')
	inProgressPagesFilename = os.path.join("data",siteName+"_InProgress.txt")
	if purge:
		print("purging file related to",siteName)
		try:
			os.remove(pagesVisitedFilename)
		except OSError:
			pass
		try:
			os.remove(urlsVisitedFilename)
		except OSError:
			pass
		try:
			os.remove(failedPagesFilename)
		except OSError:
			pass
		try:
			os.remove(redundantPagesFilename)
		except OSError:
			pass
		try:
			os.remove(completedPagesFilename)
		except OSError:
			pass
		try:
			os.remove(inProgressPagesFilename)
		except OSError:
			pass

	pageList = list()
	if os.path.exists(inProgressPagesFilename):
		pageList = load_list(inProgressPagesFilename)
		print("found in-progress page list")
	else:
		print("loading original page list")
		if os.path.exists(os.path.join("data",siteName+".txt")):
			pageList = load_list(os.path.join("data",siteName+".txt"))
		else:
			raise IOError("error! could not find a page list")
	time.sleep(1)
	urlsVisited = []
	if os.path.exists(urlsVisitedFilename):
		urlsVisited = load_list(urlsVisitedFilename)


	pagesToRemove = []
	folder = os.path.join("data",siteName+'Data')
	#%% Collect majority of pages (based on having 'References' at end of page)
	for idx, page in enumerate(pageList):
		suffix = f"{page}"
		printProgressBar(idx,len(pageList),suffix = suffix+" "*(50-len(suffix)), length = 50)	#for console
		#update_progress(idx, len(pageList)) # for jupyter notebook

		try:
			# keep track of pages already requested
			append_to_file(page, pagesVisitedFilename)
			# get url
			url = baseurl + page
			# before actually requesting the page, check if it's been visited before
			if url in urlsVisited:
				append_to_file(page, redundantPagesFilename)
			else:
				# request the page
				resp = requests.get(url)
				if not resp.ok:
					append_to_file(page, failedPagesFilename)
				else:
					# limit to 1 request every 2 seconds
					time.sleep(2)
					# get actual (redirected) url and generate filename from that
					actualurl = resp.url.split("#")[0]
					leaf = actualurl.replace(baseurl,"")
					filename = "".join(re.split('\W+',leaf))
					fullpath = os.path.join(folder,filename+"_fullText.txt")
					boldTermsPath = os.path.join(folder,filename+"_boldTerms.txt")
					headersPath = os.path.join(folder,filename+"_headerTerms.txt")

					# if we're looking at LeagueFandom, then we need to skip pages
					# that are certain categories
					isRedundant = False
					if siteName=="LeagueFandom":
						strainer = SoupStrainer(class_="page-header__categories-links")
						soup = BeautifulSoup(resp.content,features=parser,parse_only=strainer)
						for a in soup.find_all('a'):
							if 'href' in a.attrs and 'Category' in a['href']:
								category = a['href'].split(':')[1]
								if category in LeagueFandomBadCategories:
									isRedundant = True


					# check if webpage has already been collected (e.g. redirects)
					if actualurl in urlsVisited or isRedundant:
						append_to_file(page, redundantPagesFilename)
					else:
						# add to list of urls visted
						append_to_file(actualurl, urlsVisitedFilename)
						urlsVisited.append(actualurl)
						textList = list()
						linkText = list()
						boldTerms = list()
						headerTerms = list()
						for strainer in strainers:
							soup = BeautifulSoup(resp.content,features=parser,parse_only=strainer)
							for t in tagsToRemove:
								remove_tag(soup,t)
							for c in classesToRemove:
								remove_class(soup,c)
							textList.append(soup.get_text())
							# get titles from all links to other pages that don't have text
							links = soup.find_all('a')
							for idx, l in enumerate(links):
								if 'title' in l.attrs.keys() and l.string==None:
									linkText.append(l['title'])

							# get text from everything that is boldface
							for t in soup.find_all("b"):
								boldTerms.append(t.string)
							#boldTerms = list(dict.fromkeys(boldTerms))
							# get text from all headers
							for t in soup.find_all(['h1','h2','h3','h4','h5','h6']):
								headerTerms.append(t.string)
							#headerTerms = list(dict.fromkeys(headerTerms))

						# get hovertext from mobafire
						if re.search(".*mobafire.*champion.*stats",actualurl)!=None or 'abilities' in actualurl:
							print("\ndoing hovertext")
							# if we have www.mobafire.com/champion/<champion-name/stats or www.mobafire.com/abilities as the url
							hoverText = getMobaAjaxHover(resp)
							#print('--------------------------------------')
							#print(hoverText)
							textList.append(hoverText)
							#input("pausing...")

						fullText = " ".join([*textList,*linkText])
						t = re.split("\W+",fullText)
						fullText = actualurl + "\n" + " ".join(t)

						# save content to text file
						save_textFile(str(fullText), fullpath)
						write_list(boldTerms, boldTermsPath)
						write_list(headerTerms, headersPath)
						# add page to completed list
						append_to_file(page, completedPagesFilename)

				# end if actualURL not in urlsVisited
			# end not os.path.exists(p) and url not in urlsVisited
			# add page to list of files to remove
			pagesToRemove.append(page)
		except:
			e = sys.exc_info()
			# keep track of pages that failed to get data from
			append_to_file(page, failedPagesFilename)
			print("error!", e, "on",page)
			traceback.print_exc(file=sys.stdout)
			break

	# remove pages we've gone through and write those to the in-progress list
	if len(pagesToRemove)>0:
		for p in pagesToRemove:
			pageList.remove(p)
		write_list(pageList,inProgressPagesFilename)

	print("\ncomplete!")
