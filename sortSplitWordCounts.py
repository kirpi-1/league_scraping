import numpy as np
import pandas as pd
from utils import load_list, write_list, printProgressBar
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--batch', type=int, default = 500, action = 'store')
args = parser.parse_args()


# this is better utilized in a jupyter notebook
print("loading files...")
terms = load_list("data/filteredTerms.txt")
urls = load_list("data/urls.txt")
counts = np.zeros([len(urls)+1,len(terms)])
with open("data/counts.txt",'r',encoding='utf-8', errors='ignore') as f:
	idx = 0
	l = f.readline()	
	l = f.readline()
	while l!="":
		#clear_output(wait=True)
		printProgressBar(idx,len(urls)-1,length = 25, suffix = urls[idx]+" "*(100-len(urls[idx])))
		#print(idx,"of",len(urls)-1,urls[idx])
		counts[idx,:] = l.split("\t")[1:-1]
		l = f.readline()
		idx += 1
		

print("getting total sums over all sites...")
# get sum of each term over all sites
wordsums = np.zeros([counts.shape[1]])
badSums = list()
for idx in range(counts.shape[1]):
	c = np.sum(counts[:,idx])
	wordsums[idx] = c
	counts[-1,idx] = c

print("sorting...")
order = np.argsort(wordsums)

sortedTerms = list()
sortedData = np.zeros(counts.shape)

for idx in range(len(order)):
	o = order[-idx-1]
	sortedTerms.append(terms[o])
	sortedData[:,idx] = counts[:,o]
	
urls.append("Sum")
# convert to dataframe and then output to csv
batch_size = args.batch
s = 0
while s < sortedData.shape[1]:	
	e = s+batch_size
	print(s,"to",e,"of",sortedData.shape[1])
	if e > sortedData.shape[1]:
		e = sortedData.shape[1]
	df = pd.DataFrame(data = sortedData[:,s:e], columns=sortedTerms[s:e])
	df.insert(0,'site',urls)	
	df.to_csv("data/wordCounts_{}_to_{}.txt".format(s,e))	
	s += batch_size
			