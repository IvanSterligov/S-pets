from pybliometrics.scopus import ScopusSearch #pip install pybliometrics, docs are here: https://pybliometrics.readthedocs.io
import pandas as pd

query=r'affilcountry(barbados) and pubyear aft 2019' #your search query, max 5000 results

export=r'c:\temp\barbados.xlsx' #full excel path and filename to export. pip install openpyxl if using xlsx instead of xls

df=pd.DataFrame(pd.DataFrame(ScopusSearch(query, subscriber=False, verbose=True, refresh=True).results)) #download results and put them in a dataframe

df.to_excel(export, index=False) #export results

print ('exported to: ',export)