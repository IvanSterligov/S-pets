import pandas as pd
from get_counts import counts
from tqdm import tqdm
tqdm.pandas()

keypath=r'c:\ivan\key2.txt' #your api key
inpath=r'c:\temp\samplematrix.txt' #a matrix to fill, contains 1+ rows with queries and 1+columns with queries (can be empty), tab-separated, see samplematrix.txt
outpath=r'c:\temp\sample_out.csv' #where to export results, tab-separated

addon='doctype(ar or re or dp)' #this optional query is added to all queries. use for global filtering, like doctype(ar or re)

with open(keypath,'r') as f:
    key = f.read()

df=pd.read_csv(inpath, sep='\t',header=0,encoding='utf-8')

counter=0
for x in df.columns:
    if x=='entity' or x=='query':
        pass
    else:
        counter += 1
        print ('\ncolumn number:',counter,', content:', x)
        df[x]=df.progress_apply(lambda row: counts(key,(row['query']+('' if 'Unnamed:' in str(x) else (' and '+x))+((' and '+addon) if addon else ''))),axis=1)

df.to_csv(outpath, sep='\t',index=False, encoding='utf-8')
print ('exported to:', outpath)