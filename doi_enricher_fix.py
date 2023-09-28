import re
import json
import requests
from collections import Counter

#you have to provide your valid email when working with APIs, or else you are a bad, bad person

email='example@example.com'

def openalex_enrich(s, download=''): #optionally set download as path to download full jsons, i.e. 'c:\\scopets\\jsons\\' 
    listnewcols=['OpenAlex_id','OpenAlex_authornames','OpenAlex_authorships','OpenAlex_abstract','OpenAlex_topconcepts','OpenAlex_unique_RORs'] #names of added columns
    global email
    if isinstance(s['doi'],str):
        url=r'https://api.openalex.org/works/https://doi.org/'+str(s['doi'])+'?mailto:'+str(email)
        r = requests.get(url)
        if r.status_code != 404:
            rj=requests.get(url).json()          
            oa_id=rj['ids']['openalex']
            if download !='': #exports json to file
                path=download+oa_id.replace(r'https://openalex.org/','')+'.json'                
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(rj, f, ensure_ascii=False, indent=4)
            s['OpenAlex_id'] = oa_id
            authors=[]
            for x in rj['authorships']:
                if x['author']['display_name'] is not None:
                    authors.append(x['author']['display_name'])
            s['OpenAlex_authornames']= ','.join(authors) if authors else 'none'
            authorships=[]
            for x in rj['authorships']: 
                if x is not None:
                    authorships.append(x) #may break excel cell limit for mega-author papers
            s['OpenAlex_authorships']= str(authorships) if authorships else 'none' #to convert back:https://stackoverflow.com/questions/1894269/how-to-convert-string-representation-of-list-to-a-list
            abstract_list=[]
            if rj['abstract_inverted_index'] is not None:
                for x in rj['abstract_inverted_index'].keys():abstract_list.append(x)
                abstract=" ".join(abstract_list)
            else:
                abstract='none'       
            s['OpenAlex_abstract'] = abstract
            concepts_list=[]
            if rj['concepts'] is not None:
                for x in rj['concepts']: float(x['score'])>0.6 and concepts_list.append(x['display_name'])
                concepts=",".join(concepts_list)
            else:
                concepts='none'
            s['OpenAlex_topconcepts']=concepts
            s['OpenAlex_authornames']= ','.join(authors) if authors else 'none'
            rors=re.findall(r'https:\/\/ror\.org\/[A-Za-z0-9]*',r.text)
            s['OpenAlex_unique_RORs'] = ','.join(set(rors)) if rors else 'none'
        else:
            for x in listnewcols: s[x]='not_in_OpenAlex'                
    else:
        for x in listnewcols: s[x]='no_doi' 
    return s

def crossref_enrich(s, download=''): #optionally set download as path to download full jsons, i.e. 'c:\\scopets\\jsons\\' 
    listnewcols=['CrossRef_abstract', 'CrossRef_subjects'] #names of added columns
    global email
    if isinstance(s['doi'],str):
        url=r'https://api.crossref.org/works/'+str(s['doi'])+'?mailto:'+str(email)
        r = requests.get(url)
        if r.text != 'Resource not found.':
            try:
                rj=requests.get(url).json()          
                if download !='': #exports json to file
                    path=download+s['doi'].replace(r'/','_')+'.json' #replace slash with _ in doi to make a valid filename                
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(rj, f, ensure_ascii=False, indent=4)
                s['CrossRef_abstract']=re.sub('<[^<]+?>', '', rj['message']['abstract']) if 'abstract' in rj['message'] else 'no_abstract'
                s['CrossRef_subjects']=','.join(rj['message']['subject']) if 'subject' in rj['message'] else 'no_subjects'
            except Exception as e:
                for x in listnewcols: s[x]='error:'+str(e)
        else:
            for x in listnewcols: s[x]='not_in_CrossRef'                
    else:
        for x in listnewcols: s[x]='no_doi' 
    return s

def ss_enrich(s):
    listnewcols=['SS_id','SS_abstract','SS_TLDR','SS_AI_field','SS_AI_fields_from_references'] #names of added columns
    global email
    fields='authors,tldr,abstract,s2FieldsOfStudy,references.s2FieldsOfStudy' #fields to query from SS api
    doi=s['doi']
    if isinstance(doi,str):
        url=r'https://api.semanticscholar.org/graph/v1/paper/'+str(doi)+'?fields='+fields
        #print (url)
        rj = requests.get(url).json()
        if not 'error' in rj:
            s['SS_id']=rj['paperId'] if 'paperId' in rj else 'no_id_error'
            s['SS_authors']=str(rj['authors']) if 'authors' in rj else 'no_authors'
            s['SS_abstract']=rj['abstract'] if 'abstract' in rj else 'no_abstract'
            s['SS_abstract']='no_abstract' if s['SS_abstract']==None else s['SS_abstract']
            s['SS_AI_field']=str(rj['s2FieldsOfStudy']) if 's2FieldsOfStudy' in rj else 'no_AI_field'
            s['SS_TLDR']=rj['tldr']['text'] if rj['tldr'] is not None else 'no_tldr'
            s['SS_TLDR']='no_tldr' if s['SS_TLDR']==None else s['SS_TLDR']
            if 'references' in rj:
                refs=[]
                for x in rj['references']:
                    if x['s2FieldsOfStudy'] is not None:
                        for y in x['s2FieldsOfStudy']:
                            if y['source']=='s2-fos-model':
                                refs.append(y['category'])
                s['SS_AI_fields_from_references']=str(Counter(refs)).replace('Counter({','').replace('})','') if Counter(refs) else 'no_refs_or_no_fields_in_refs'
            else:
                s['SS_AI_fields_from_references']='no_refs'
        else:
            #print (rj['error'])
            for x in listnewcols: s[x]='not_in_SS'                
        return s
    else:
        for x in listnewcols: s[x]='no_doi' 
        return s