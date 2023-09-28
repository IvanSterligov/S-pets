import datetime
import requests
import json

with open(r'c:\ivan\key2.txt','r') as f: #path to the file with your api key    
    key = f.read()

#query=r'af-id(60014966) and source-id(19700182758) and pubyear is 2022 and doctype(ar or re or dp)' #put your advanced search query here
query=r'(affilcountry(india) and affilcountry(united kingdom)' #put your advanced search query here

fullquery=r'https://api.elsevier.com/content/search/scopus?start=0&count=1&query='+str(query)+'&apiKey='+str(key)

print('url:',fullquery)

r = requests.get(fullquery)
print (r.headers)
rj=r.json()

print ('remaining API quota: ',r.headers['X-RateLimit-Remaining']) #how many requests left
print ('resets at: ',datetime.datetime.fromtimestamp(int(r.headers['X-RateLimit-Reset']))) #when they reset
print('query: ',query, '\nquery length:', len(query))
#print ('URL: ',fullquery, len(fullquery))

print('results: ',rj['search-results']['opensearch:totalResults']) #number of results
#uncomment to print json sample
#print ('json:','\n',json.dumps(rj,indent=4)) #a sample of results
