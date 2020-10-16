# Counts the number of occurances of each word in the filteredTerms.txt file
# By searching through the text data from each link

import numpy as np
import os, re
from utils import load_list, write_list, printProgressBar

sites=['gamepedia','LeagueFandom','mobafire']

# get the list of all full text files for all sites
files = list()
for site in sites:			
	folder = os.path.join("data",site+"Data")
	filelist = os.listdir(folder)
	files = files + [os.path.join(folder,b) for b in filelist if "fullText" in b]	

# get the words to count
terms = load_list("data/filteredTerms.txt")
urls = list()
counts = np.zeros([len(files),len(terms)])
countFilename = "data/counts.txt"

removeText = load_list('removeText.txt')


# Write the first line of the counts filename, which is terms
with open(countFilename,'w+',encoding = 'utf-8',errors='ignore') as f:
	f.write("site\t")
	for t in terms:
		f.write(t+"\t")
	f.write("\n")



# main loop
for idx, file in enumerate(files):	
	#printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	printProgressBar(idx,len(files)-1,suffix = file+" "*(80-len(file)), length=50)
	
	text = ""
	with open(file, 'r', encoding='utf-8',errors='ignore') as f:				
		text = f.read()		
		# remove the first line, which is the source url and add it to urls list
		url = re.match(".*\n",text)[0]
		urls.append(url.strip())
		# remove 1 endline character
		text = re.sub(".*\n","",text,count=1)
		text = text.lower()
		# remove skin titles
		for s in removeText	:
			text = text.replace(s.lower(),'')		
		# add a space character to front and back so that full word search works for first and last
		text = " " + text + " "
		for jdx, t in enumerate(terms):
			# only count full word matches (
			count = text.count(f" {t} ")		
			counts[idx][jdx] = count
	# write the counts
	with open(countFilename,'a+', encoding = 'utf-8',errors='ignore') as f:
		f.write(urls[idx])
		f.write('\t')
		for c in counts[idx]:
			f.write(str(int(c))+"\t")
		f.write("\n")

write_list(urls,"data/urls.txt")
print("done!")