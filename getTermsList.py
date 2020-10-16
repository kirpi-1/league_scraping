import utils
import re
files = ["data/mobafire_CompletedPagesList.txt"]
pages = utils.load_list(files[0])
terms = set()
for p in pages:
	words = p.split('/')
	for w in words:
		if '-' in w:
			# replace '-' with ' ' 
			w = w.split('-')
			# remove the last part if it is a number or "guide"
			if w[-1] == 'guide' or w[-1].isnumeric():
				w = w[:-1]
			w = " ".join(w)
		terms.add(w.lower().strip())
mobafireTermsList = list(terms)
mobafireTermsList.sort()

file = "data/LeagueFandom_CompletedPagesList.txt"
pages = utils.load_list(file)
terms = set()
termsToReplace = [('_',' '),('%27','\''),('(item)',''),('%26','&')]
for p in pages:
	if "Teamfight_Tactics" in p:
		continue
	words = p.split('/')
	for w in words:
		
		for t in termsToReplace:
			w = w.replace(t[0],t[1])
		w = re.sub('\(.*\)','',w)
		terms.add(w.lower().strip())
fandomTermsList = list(terms)
fandomTermsList.sort()   


# Gamepedia
file = "data/gamepedia_CompletedPagesList.txt"
pages = utils.load_list(file)
terms = set()
termsToReplace = [('_',' '),('%27','\''),('(item)',''),('%26','&')]
for p in pages:
	if "Teamfight_Tactics" in p:
		continue
	words = p.split('/')
	for w in words:
		for t in termsToReplace:
			w = w.replace(t[0],t[1])
		w = re.sub('\(.*\)','',w)
		terms.add(w.lower().strip())
gamepediaTermsList = list(terms)
gamepediaTermsList.sort()


terms = set.union(set(mobafireTermsList), set(fandomTermsList),set(gamepediaTermsList))
termsList = list(terms)
termsList.sort()
utils.write_list(termsList, "data/termsList.txt")