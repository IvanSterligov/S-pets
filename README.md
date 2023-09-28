S-pets is a bunch of simple python scripts intended to work with [Scopus](https://www.scopus.com) without a subscription. It utilises free API natively and also uses a nice library called [Pybliometrics](https://pybliometrics.readthedocs.io) for some calls, so pip install pybliometrics. 

[Scopus Advanced Search syntax and field codes](https://dev.elsevier.com/sc_search_tips.html)

[General Scopus API specification](https://dev.elsevier.com/sc_api_spec.html). Please follow Scopus API usage rules.

[get API key](https://dev.elsevier.com/apikey/manage) (some countries seem to be banned by geoIP)

Quota as of 02\2023 is 20000 api calls per week.

Put all these scripts in the same folder. Put your api key in key.txt and edit the path to it accordingly. Also, Pybliometrics will ask for an api key once.

S-pets is used in several science of science projects by [Ivan Sterligov](https://scholar.google.com/citations?user=HApth4AAAAAJ&hl=en), its author.  

Contents:

### simplequery.py

The simplest script meant to test queries. Produces a number of results found, a sample in JSON, your api key remaining quota and quota reset date.

### get_counts.py

This function counts the number of search results per scopus advanced search query. Usage is simple: counts(key,query). It is required (imported) by most other scripts. Does not use Pybliometrics. 
```
from get_counts import counts
key=your api key
query=your advanced search query
print (counts(key,query))
```
### get_metrics.py

This function produces a dict with a query and simple metrics for a set of publications conforming to a given scopus advanced search query. Max 5000 papers for a non-subscriber!
Metrics are: 
- pub_count (total publications)
- article_count (articles only)
- total_cites
- max_cites_per_paper
- h_index
```
from get_metrics import metrics
print (metrics('AU-ID(16422603600)'))

{'search_query': 'AU-ID(16422603600)', 'pub_count': 8, 'article_count': 8, 'total_cites': 338, 'max_cites_per_paper': 170, 'h_index': 5}
```
### get_publist.py

This saves results of a search query to an excel file (1 publication = 1 row). Columns are: 

eid,doi,title,subtype,subtypeDescription,creator,affilname,affiliation_city,affiliation_country,coverDate,coverDisplayDate,publicationName,issn,source_id,aggregationType,volume,issueIdentifier,pageRange,citedby_count,openaccess,freetoread,freetoreadLabel. 

See Pybliometrics docs for [more info](https://pybliometrics.readthedocs.io/en/stable/classes/ScopusSearch.html).

### get_publist_enrich.py

The same as **get_publist** + also tries to add more metadata fields from OpenAlex, Semantic Scholar and CrossRef via their native APIs using DOIs. Can be quite time-consuming for large paper sets, so an async version is on the way.

These are added:

- CrossRef_abstract
- CrossRef_subjects
- OpenAlex_abstract
- OpenAlex_authornames
- OpenAlex_authorships
- OpenAlex_id
- OpenAlex_topconcepts
- OpenAlex_unique_RORs
- SS_AI_field
- SS_AI_fields_from_references
- SS_TLDR
- SS_abstract
- SS_authors
- SS_id

Note that for many papers many of these fields will be empty. 

If you want to export not to Excel but to csv, note that you are often dealing with messy abstracts with newlines and carriage returns. 

**jsonpath** = optional arg. Set to a valid path like r'c:\export\jsons\' to download full JSONs from OpenAlex (filename=paper id) and CrossRef (filename=doi with \ replaced by _ )

### doi_enricher_fix.py

A set of functions required for **get_publist_enrich**. You can add some fields or otherwize tinker with it if you need. Please be polite and specify a valid email here to be used for API calls to OpenAlex, Semantic Scholar and CrossRef. 

### count_matrix.py

Takes a table with queries in 'query' column and intersects them with queries in the names of other columns. Also has an optional  global query addon intersected with all other queries. Uses get_counts.py.

For example, you cam provide a list of authors in the query column, and add columns with queries for different publication periods. This script will fill the cells with paper counts for intersecting queries, like **'af-id(12345678) and pubyear is 2010'** for the top-left cell. 

| query           | pubyear is 2010 | pubyear is 2011 | pubyear aft 2011 |
|-----------------|-----------------|-----------------|------------------|
| af-id(12345678) | 2               | 3               | 7                |
| af-id(12345679) | 0               | 1               | 9                |
| af-id(12345688) | 5               | 0               | 0                |


### metrics_matrix.py

Same as counts_matrix, but fills the query intersection cells with one of the specified citation metrics using the **get_metrics** described earlier. 
Note that this consumes much more queries than simple counting because we need to download metadata for each paper to get its citation counts.

### queryXid.py

This one filters publication counts for a given set of search queries using a given list of Scopus sources.

**path** = path to the list of Scopus advanced search queries as a tab-separated table with the obligatory column "query", or just a text file with "query" in the first line and queries in other lines.

**sourcepath** = path to the list of sources to count papers in, as a tab-separated table with columns containing scopus source-id and column names as list labels

Note that the list should contain Scopus source-ids, not ISSNs. You can get these ids [here](https://www.scopus.com/sources.uri). For example, you can make a list containing journals of several publishers (each in a separate column) and use it to collect paper counts per publisher for your queries. 

Use a script **listmaker.py** to prepare your source lists (info inside).

**outpath** = path to export results

**query** = an additional Scopus search query to add to every query (use to filter by year, doctype). Can't be empty.

That's all for now.

Thanks to Elsevier for the free Scopus API and to Pybliometrics team. Peace. 




