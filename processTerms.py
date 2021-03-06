import os, re, sys
from utils import load_list, write_list
import argparse

# script in order to get terms and process them
# uses completedPagesList for each site to construct a list of terms
# optionally uses bold and header terms from each page
# replaces html substitutes with actual characters (e.g. replace %27 with a single quote ')
# fixes some character issues (unusual single quotes or characters)
# removes common stopwords from the list of terms
# removes champion names, item names, location names, and skin names from the list
# removes undesired pages such as version history ("Vx.x" pages)
# removes other errors in terms
# finally removes duplicates
# author: Zack Wisti

stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
			 "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
			 "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
			 "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
			 "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
			 "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
			 "with", "about", "against", "between", "into", "through", "during", "before", "after", "above",
			 "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further",
			 "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
			 "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
			 "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
championList = load_list('championList.txt')
championList = [b.lower() for b in championList]
itemList = load_list('itemList.txt')
itemList = [b.lower() for b in itemList]
def filterTerms(terms,banlist=None):
	terms = [b.lower() for b in terms]
	# get the stem from any thing that is directory format
	bonus = list()
	for b in terms:
		if "/" in b:
			bonus += b.split("/")
	terms += bonus		
	terms = [b for b in terms if not "/" in b]
	
	# replace _ with a space
	terms = [re.sub("_"," ", b) for b in terms]
	# replace %26 with an ampersand
	terms = [re.sub("%26","\&", b) for b in terms]
	# replace amp with an ampersand
	terms = [re.sub(" amp "," \& ", b) for b in terms]
	
	# replace %27 with a single quote
	terms = [re.sub("%27","\'", b) for b in terms]	
	# remove sentences
	terms = [b for b in terms if len(b.split(" "))<=6]	
	
	# remove things that have no characters in them
	terms = [b for b in terms if re.search("[a-z]+",b)!=None]
	terms = [b for b in terms if len(b)>1]
	
	# uses look-ahead (?=...) and look-behind (?!...) to match [a-z]-[a-z] and replace it with a space
	terms = [re.sub("[-–](?=[a-z])(?!=[a-z])"," ", b) for b in terms]
	
	# remove things that start and end with [],(), and "" or are broken and start/end with only one
	terms = [b for b in terms if re.match("[\(\"\[“].*[\)\"\]”]$",b)==None]
	#remove trailing colon
	terms = [re.sub("(\'s)|:$","",b) for b in terms]
	#terms = [b for b in terms if re.match(".*[\)\"\]”]",b)==None]
	#terms = [b for b in terms if re.match("[\(\"\[“].*",b)==None]
	
	# remove things that start with / and .
	#terms = [b for b in terms if re.match("[\./]",b)==None]
	
	# ---------- delete key phrases section ----------
	
	# remove champions
	for champion in championList:
		terms = [b for b in terms if re.match(f"{champion}",b)==None]
		terms = [b for b in terms if re.match(f"{champion}-\d+",b)==None]
		terms = [b for b in terms if re.match(f"{champion} guide",b)==None]
	
	# remove items
	for item in itemList:
		terms = [b for b in terms if re.match(f"{item}",b)==None]
		
	# remove chromas
	terms = [b for b in terms if re.search("chroma",b)==None]	
	# ---------- final cleanup section ----------
	terms = [b.strip() for b in terms]
	
	# remove words in the banlist and stopwords
	if banlist != None:
		terms = [b for b in terms if b not in banlist]
	terms = [b for b in terms if not b in stopwords]
		
	# remove season X
	terms = [b for b in terms if re.match("season \d+",b)==None]
	terms = [b for b in terms if re.match("season one|two|three|four|five|six|seven|eight|nine|ten",b)==None]
		
		
	# remove things like v4.5 and V0.9.8.1
	terms = [b for b in terms if re.match("[vV][\d*\.]+",b)==None]
	# remove Patch xx.xx items
	terms = [b for b in terms if re.match("patch \d*\.\d*",b)==None]	
	# remove more patch terms
	terms = [b for b in terms if re.match("league of legends v*[0-9]+",b)==None]
	
	removeList = ['champion insights:','champion reveal:','champion roadmap:','champion update:','champion sneak peak:',
				  '\(rune\)','\(item\)','\(passive\)','\(legends of runeterra\)','\(disambiguation\)',
				  '\(teamfight tactics\)','\(little legend\)','\(wild rift\)','\(trinket\)']
	terms = [re.sub("|".join(removeList),"",b) for b in terms]
	# replace the weird single quote with regular single quote
	terms = [b.replace("’","'") for b in terms]	
	# remove FirstName 'nickname' LastName entries
	terms = [b for b in terms if re.match("\D+ \'\S+\' \D+",b)==None]
	
	# remove dates
	terms = [b for b in terms if re.match("(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)] \d+",b)==None]
	
	# remove "Passive - "
	terms = [re.sub("passive [-–]","",b) for b in terms]
	
	# delete "Q/W/E/R - Spell Name"
	terms = [re.sub("^[qwer] [-–] ","", b) for b in terms]	
	
	# remove +number% of like +10% of max life
	terms = [re.sub("\+*\d+%*( of ).*","",b) for b in terms]
	terms = [re.sub("\'s$","",b) for b in terms]
	terms = [re.sub("\'$","",b) for b in terms]   		
	
	# remove duplicates
	terms = list(dict.fromkeys(terms))
	terms.sort()
	return terms


# command line arguments for (re)processing using header and bold terms
# default is to not use header/bold terms
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--reprocess', default = False, action = 'store_true')
parser.add_argument('-b', '--bold', default = False, action = 'store_true')
parser.add_argument('-d', '--header', default = False, action = 'store_true')
args = parser.parse_args()
reprocess = args.reprocess
termTypeNames = ["bold", "header"]
if reprocess:
	print("reprocessing terms from source files...")
	# collect bold and header terms
	sites=['gamepedia','LeagueFandom','mobafire']
	for site in sites:
		terms = list()
		folder = os.path.join("data",site+"Data")
		files = os.listdir(folder)
		boldFiles = [b for b in files if "boldTerms" in b]
		headerFiles = [h for h in files if "headerTerms" in h]
		fileLists = [boldFiles, headerFiles]
		# termTypeNames defined above
		for j, filelist in enumerate(fileLists):
			for idx, filename in enumerate(filelist):
				#clear_output(wait=True)
				print("processing", site,":",termTypeNames[j],": {} of {}".format(idx,len(filelist)-1) )
				try:
					terms = terms + load_list(os.path.join(folder,filename))
				except:
					e = sys.exc_info()
					print(e)
					print(os.path.join(folder,filename))                    
			write_list(terms, os.path.join("data",site+"_"+termTypeNames[j]+"Terms.txt"))
	print("done!")


# load all the terms
print("loading terms from preprocessed files...")
sites = ['gamepedia','LeagueFandom','mobafire']
files = ['_CompletedPagesList.txt']
if args.bold:
	files.append('_boldTerms.txt')
if args.header:
	files.append('_headerTerms.txt')
terms = list()

# for each site, for each set of terms
# filter them according to the function above
for site in sites:
	print("loading",site,"...")
	for file in files:		
		filename = os.path.join("data",site+file)
		tmp = load_list(filename)
		if 'mobafire_CompletedPagesList.txt' in filename:
			tmp = [re.sub("[-–]\d+$","",b) for b in tmp]
		terms = terms + tmp
skinNames = load_list("championSkinsList.txt")	
properNouns = load_list("properNames.txt")
banlist = [*skinNames,*properNouns]
banlist = [b.lower() for b in banlist]
print("filtering terms...")
filtered_terms = filterTerms(terms, banlist)
print("filtered to",len(filtered_terms),"/",len(terms),"terms")
write_list(filtered_terms,'data/filteredTerms.txt')
