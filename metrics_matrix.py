import pandas as pd
from get_metrics import metrics
from tqdm import tqdm
tqdm.pandas()

inpath=r'c:\temp\samplematrix.txt' #a matrix to fill, should contain 1+ rows with queries and 1+columns with queries, tab-separated, see samplematrix.csv
outpath=r'c:\temp\samplematrix_out.csv' #where to export results
metric='total_cites' #which metric to produce. possible variants: pub_count, article_count, total_cites, max_cites_per_paper, h_index
addon='doctype(ar or re or dp)' #this optional query is added to all queries. use for global filtering, like doctype(ar or re).

df=pd.read_csv(inpath, sep='\t',header=0,encoding='utf-8')

for x in df.columns:
    if x=='entity' or x=='query':
        pass
    else:
        df[x]=df.progress_apply(lambda row: metrics(row['query']+('' if 'Unnamed:' in str(x) else (' and '+x))+((' and '+addon) if addon else ''))[metric],axis=1)

df.to_csv(outpath, sep='\t',index=False, encoding='utf-8')
print ('exported to: ',outpath)