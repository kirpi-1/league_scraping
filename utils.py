import requests, time, sys, os, bs4, traceback, re
from bs4 import BeautifulSoup, SoupStrainer

# This file is for encapsulating certain common functions
# and to provide the space for reusable, functioning code
# There are utilities for list reading/writing as well as
# functions used for processing and filtering the text from
# a list of webpages.



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

# write a list to file as text, one list item per line
def write_list(l, filename):
	filename = add_txt_ext(filename)
	if os.path.dirname(filename)!='':
		os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename,'w',encoding='utf-8',errors='ignore') as f:
		for item in l:
			f.write(str(item)+'\n')
			
# load a list of text to file, one list item per line
def load_list(filename):
	out = []
	with open(filename,'r', encoding='utf-8', errors ='ignore') as f:
		l = f.readline()
		while l!="":
			l = l.strip()
			out.append(l)
			l = f.readline()
	return out

# append a value or list of values to a file
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

# add the ".txt" extention to a filename if it does not already have it
def add_txt_ext(filename):
	path,ext = os.path.splitext(filename)
	if ext != "txt":
		filename = path+".txt"
	return filename

# function to remove text/data of a particular class from a soup object
def remove_class(soup, class_):
	found = True
	while found:
		found = remove_class_h(soup, class_)

# helper function to remove text/data
# returns true if it found an instance of the class and removed it
# returns false if it did not find an instance of the class
def remove_class_h(soup, class_):
	for desc in soup.descendants:
		if type(desc) == bs4.element.Tag and 'class' in desc.attrs.keys():		
			if class_ in " ".join(desc['class'][:]):
				desc.decompose()
				return True
	return False

# function to remove text/data from a particular html tag (e.g. "script")
def remove_tag(soup, tag):
	for script in soup([tag]):
		script.decompose()

# Function for printing progress bar
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

# function to get text from hovertext functions on mobafire
def getMobaAjaxHover(page):	
	soup = BeautifulSoup(page.content,'lxml')
	# find the ajax tooltip tags
	tags = soup.find_all(class_=['ajax-tooltip','tooltip-ajax'])
	tmp_text = list()
	# for each tooltip on the page, get the tagname and index number
	# then access the corresponding page on mobafire to download the text associated with that tooltip
	for idx, tag in enumerate(tags):
		printProgressBar(idx+1,len(tags),length = 30, prefix="\t")#for console
		ajax_string = None
		# find tooltip name ("t") and index ("i")		
		for c in tag['class']:
			if re.search(".*t:.*i:.*",c)!=None: # find the one that is like '{t:ReforgedRune,i:61}'
				ajax_string = c
				break
		# if we couldn't find one, then skip to the next tag
		if ajax_string == None:
			continue
		# process the text in order to get the name and index
		tmp = ajax_string.split(',')[0]#t:ReforgedRune
		t = tmp[tmp.find("t:")+2:tmp.find(",")].replace("'","")
		tmp = ajax_string.split(',')[1]#61
		i = c[c.find("i:")+2:c.find("}")].replace("'","")
		# if it is not information about a champion skin, then request the page content and get all the text
		if t != "SkinDetails":
			cURL=f"https://www.mobafire.com/ajax/tooltip?relation_type={t}&relation_id={i}"
			#print(cURL)
			indRunePage = requests.get(cURL)
			indRuneSoup = BeautifulSoup(indRunePage.content,'lxml')
			tmp_text.append(indRuneSoup.text.strip().replace('\n',' '))
	# end for tag in tags
	hover_text = " ".join(tmp_text)
	return hover_text

LeagueFandomBadCategories = ['Legends_of_Runeterra','Contracted_artists','Riot_Games_staff',
            'Events','Tournaments','WR_finished_items','Anniversary', 'Wild_Rift','Teamfight_Tactics']

def mine_words(siteName, baseurl, strainers, tagsToRemove, classesToRemove, parser='lxml',purge=False):
	# main workhorse function to extract data
	pagesVisitedFilename = os.path.join("data",siteName+"_PagesVisitedList.txt")
	urlsVisitedFilename = os.path.join("data",siteName + '_UrlsVisitedList.txt')
	failedPagesFilename = os.path.join("data",siteName + '_FailedPagesList.txt')
	redundantPagesFilename = os.path.join("data",siteName + '_RedundantPagesList.txt')
	completedPagesFilename = os.path.join("data",siteName + '_CompletedPagesList.txt')
	inProgressPagesFilename = os.path.join("data",siteName+"_InProgress.txt")
	# if purge flag is set, start over from the beginning, deleting all in-progress files
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
	# for each page in teh pagelist, try requesting it
	# if there's an error, catch it and add the page to the failedPages list
	# if successful, process it
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
			# if so, add to redundant pages and go next
			# if not, then actually request the page
			if url in urlsVisited:
				append_to_file(page, redundantPagesFilename)
			else:
				# request the page
				resp = requests.get(url)
				# if the request failed, add it to the failedPages list
				if not resp.ok:
					append_to_file(page, failedPagesFilename)
				else:
					# limit to 1 request every 2 seconds
					time.sleep(2)
					# sometimes a URL redirects you to another page, the "true" URL for that page
					# so, we will record that
					# get actual (redirected) url and generate filename from that
					actualurl = resp.url.split("#")[0]
					leaf = actualurl.replace(baseurl,"")
					# set up files for saving data
					filename = "".join(re.split('\W+',leaf))
					fullpath = os.path.join(folder,filename+"_fullText.txt")
					boldTermsPath = os.path.join(folder,filename+"_boldTerms.txt")
					headersPath = os.path.join(folder,filename+"_headerTerms.txt")					
					

					# if we're looking at LeagueFandom, then we need to skip pages
					# that are certain categories
					# the categories are defined in this file (utils.py)
					# if the page is in one of these categories, then we mark it as redundant (and don't process it)
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
					# or if it is from LeagueFandom and on the banlist of categories
					# if so, add to redundantPagesFilename
					# if not, go on to actually process it
					if actualurl in urlsVisited or isRedundant:
						append_to_file(page, redundantPagesFilename)						
					else:
						
						# add to list of urls visted
						append_to_file(actualurl, urlsVisitedFilename)
						urlsVisited.append(actualurl)					
						# set up lists for terms
						textList = list()
						linkText = list()
						boldTerms = list()
						headerTerms = list()
						# for each strainer, get the soup from the page
						# remove data from tags you don't want
						# remove data from classes you don't want
						# then from the result, add the text to the textList
						# also record all bold text, all header text, and the lext of every link
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
							textList.append(hoverText)
							
						# join all the text together, then remove all whitespace and put a single space between each word
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
