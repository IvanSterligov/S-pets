from pybliometrics.scopus import ScopusSearch #pip install pybliometrics, docs are here: https://pybliometrics.readthedocs.io
import pandas as pd

#produces a dict with simple metrics for a set of publications conforming to a given scopus advanced search query. Max 5000 papers for a non-subscriber.
#metrics are: pub_count, article_count, total_cites, max_cites_per_paper, h_index

def metrics (query): #use author_id to query author, like 'AU-ID(7005509332)'
    try:
        res=ScopusSearch(query, subscriber=False, verbose=True)
        if res.get_results_size() > 0:
            df=pd.DataFrame(pd.DataFrame(res.results))
            cites=df['citedby_count'].tolist() #a list of the citation counts of all items
            return dict(search_query=query,pub_count=len(cites),article_count=len(df[df['subtype'] == 'ar']),total_cites=sum(cites),max_cites_per_paper=max(cites),h_index=sum(x >= i + 1 for i, x in enumerate(sorted(cites, reverse=True))))
        else: #if zero publications found, returns zeros 
            return dict(search_query=query,pub_count=0,article_count=0,total_cites=0,max_cites_per_paper=0,h_index=0)
    except Exception as e:
        print (str(e))