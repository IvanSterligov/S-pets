from pybliometrics.scopus import ScopusSearch #pip install pybliometrics, docs are here: https://pybliometrics.readthedocs.io
from doi_enricher_fix import openalex_enrich, crossref_enrich, ss_enrich
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

query='au-id(16422603600) and pubyear aft 1990' #your Scopus Advanced Search query, max 5000 results. ann 'and doi(10*)' to ensure only papers with dois are collected
export=r'c:\temp\perelman_enriched.xlsx' #full excel path and filename to export. pip install openpyxl if using xlsx instead of xls
jsonpath='' #optional. set to a valid path like 'c:\\export\\jsons\\' to download full JSONs from OpenAlex and CrossRef

print ('querying Scopus and downloading metadata (max 5000 results):')
df=pd.DataFrame(pd.DataFrame(ScopusSearch(query, subscriber=False, verbose=True).results)) #download results and put them in a dataframe
print ('enriching via OpenAlex:')
try:
    df=df.progress_apply(openalex_enrich, axis=1, args=(jsonpath,)) #don't forget to put comma after args, like args=(jsonpath,)
except Exception as e:
    print ('error:',str(e))
print ('enriching via CrossRef:')
try:
    df=df.progress_apply(crossref_enrich, axis=1, args=(jsonpath,)) 
except Exception as e:
    print ('error:',str(e))
print ('enriching via Semantic Scholar:')
try:
    df=df.progress_apply(ss_enrich, axis=1)
except Exception as e:
    print ('error:',str(e))

df.sort_index(axis=1, inplace=True)

df.to_excel(export, index=False) #export results

print ('exported to: ',export)