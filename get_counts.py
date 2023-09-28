import requests
import time

def counts(key,query): #key=your api key, query=scopus advanced search query like 'affilcountry(russia*)'
    try:
        url=r'https://api.elsevier.com/content/search/scopus?start=0&count=1&query='+str(query)+'&apiKey='+str(key)
        r=requests.get(url)
        #print (url)
        #print (r.status_code)
        #print (r.headers)
        return r.json()['search-results']['opensearch:totalResults']
    except:
        try:
            print ('some error, trying again...')
            time.sleep(2)
            url=r'https://api.elsevier.com/content/search/scopus?start=0&count=1&query='+str(query)+'&apiKey='+str(key)
            r=requests.get(url)
            return r.json()['search-results']['opensearch:totalResults']
        except Exception as e:
            print ('error:',str(e))
            