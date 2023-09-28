'''
turns a table like this:
id  discipline
1   math
2   bio
3   math
4   geo

into this:

math    bio geo
1       2   4
3
'''

import pandas as pd
import numpy as np

# Load input table
df=pd.read_csv(r'c:\temp\rus_publishers.csv', sep='\t', header=0)

# Create a dictionary where keys are disciplines and values are lists of scopus_ids
discipline_dict = df.groupby('discipline')['id'].apply(list).to_dict() #change headers accordingly if necessary

# Convert the dictionary to a DataFrame
df_result = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in discipline_dict.items() ]))

# Replace NaNs with an empty string
df_result = df_result.replace(np.nan, '', regex=True)

# Change float to int 
def float_to_int(val):
    if isinstance(val, float) and val > 0:
        return int(val)
    return val

df_result = df_result.applymap(float_to_int)

print (df_result.head())

# Export to a tab-separated csv file
df_result.to_csv(r'c:\temp\rus_publishers_out.csv', sep='\t', index=False)