#a function to get publication counts for a list of orgs\authors\countries and several lists of sources
#russian org ids are here: https://zenodo.org/record/5136473/files/v.1.1.1_table6_scopus.csv?download=1

import pandas as pd
from get_counts import counts
from requests.utils import requote_uri
from tqdm import tqdm
tqdm.pandas()

keypath=r'c:\ivan\key2.txt' #your scopus api key
path=r"c:\temp\query_orgs.csv" #path to the list of scopus advanced search queries as a tab-separated table with the obligatory column "query". 
sourcepath=r"c:\temp\sources.csv" #path to the list of sources to count papers in as a tab-separated table with columns containing scopus source-id and column names as list labels
outpath=r"c:\temp\query_orgs_out.csv" #path to export results
query=" and doctype(ar or re or dp) and pubyear is 2023" #a scopus search query to add to the general query (use to filter by year, doctype). has to be not empty.

with open(keypath,'r') as f:
    key = f.read()

def urlen(x): #helper func to get length of url-encoded strings
    return len(requote_uri(str(x)))

df=pd.read_csv(path, sep='\t', header=0, encoding='utf-8', dtype=str)
sdf=pd.read_csv(sourcepath, sep='\t', header=0, encoding='utf-8', dtype=str)

max_query_length = df['query'].apply(urlen).max() #calculate the longest query. here's the room for future improvement: we can recreate final queries for each query in the input table

def create_strings(numbers): #function to make scopus queries from long lists of journal ids
    suffix = " or "
    max_length = 2450-(urlen(query)+max_query_length) #set max query length

    result_strings = []
    current_string = ""

    for num in numbers:
        af_id_string = f"{num}{suffix}"

        if urlen(current_string) + urlen(af_id_string) > max_length:
            # Remove trailing ' or ' from the current string and add it to the result list
            current_string = current_string[:-4]
            result_strings.append(current_string)
            current_string = ""

        current_string += af_id_string

    if current_string:
        # Remove trailing ' or ' from the last string and add it to the result list
        current_string = current_string[:-4]
        result_strings.append(current_string)
    
    outlist=["source-id("+x+")"+query for x in result_strings]
    #print (outlist)
    print ("total sources:", len(numbers), "total chunks:", len(outlist))
    return outlist

def listcounter(id,key,queries): #func to do the counting on top of single 'counts' func
    counter=0
    for x in queries:
        res=counts(key,"("+str(id)+") and ("+x+")")
        #print ('chunk:',res)
        counter += int(res)
    #print ('total:',counter)
    return counter

for index, column in enumerate(sdf):
    colname=str(column)
    rawlist = sdf[column].tolist()
    cleanedList = [x for x in rawlist if x==x]    
    print ('processing column:',colname,"which is", index+1, "of",str(len(sdf.columns)))
    queries = create_strings(cleanedList)
    df[colname]=df['query'].progress_apply(listcounter, args=(key,queries))

print (df.head())

df.to_csv(outpath, sep='\t', encoding='utf-8', index=False)
print ("exported to:",outpath)