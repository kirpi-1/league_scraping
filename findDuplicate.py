import utils
import nltk

filteredTerms = utils.load_list('data/filteredTerms.txt')
filteredTerms.sort()

dupeList = dict()

for idx, t in enumerate(list(filteredTerms)):
    surroundingWords = filteredTerms[idx-3:idx+3]
    l = [a for a in surroundingWords if t!=a and nltk.edit_distance(t,a) <= 1]
    if len(l) > 0:
        dupeList[t] = l

for d in dupeList:
    print(d, dupeList[d])





keys = list(dupeList.keys())

dupeList['attack']
ing = [word for word in filteredTerms if 'ing' in word]
sWords = [word for word in filteredTerms if 's' == word[-1] and '\''!= word[-2]]



nltk.edit_distance('ability','abilities')

for t in filteredTerms:
    l = [a for a in filteredTerms if nltk.edit_distance(t,a) < 5]
    dupeList[t] = l

acroynm['cc'] = ['crowd control']
acroynm['cd'] = ['cooldown','cool down']



tlas = [f for f in filteredTerms if len(f)<=3]
acroynm['cc'] = ['crowd control']
acroynm['cd'] = ['cooldown','cool down']
acronym['aa'] = ['auto-attack', 'auto-attacks', 'auto-attacking', 'autoattacks','autoattack','autoattacking', 'auto attack','auto attacks', 'auto attacking']




aa,auto attack
aas, archangels staff
