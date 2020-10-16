import os
import utils

# collect bold and header terms
sites=['gamepedia','LeagueFandom','mobafire']

for site in sites:    
    terms = list()    
    folder = os.path.join("data",site+"Data")
    files = os.listdir(folder)
    boldFiles = [b for b in files if "boldTerms" in b]
    headerFiles = [h for h in files if "headerTerms" in h]
    fileLists = [boldFiles, headerFiles]
    termTypeNames = ["bold", "header"]
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
        utils.write_list(terms, os.path.join("data",site+"_"+termTypeNames[j]+"Terms.txt"))
print("done!")