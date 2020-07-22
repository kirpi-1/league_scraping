## Order of execution

### Get the page urls
get<site>Pages.py

### Get text from pages
extract<site>Content.py
-p, --purge			Purge any in-progress list and start from the beginning. Default false (looks for in-progress page list and starts there)

### Create terms list
processTerms.py - can choose whether or not to include bold/header terms
-r, --reprocess		Reapply the filtering process to the source terms. Default false (uses existing preprocessed list)
-b, --bold			Include bold terms. Default false
-d, --header		Include header terms. Default false
### Get word counts
countWords.py

### sort and split word counts
sortSplitWordCounts.py

