import pandas as pd

# file to make dataframe out of csv file over plants and their scientific name

df = pd.read_csv('cites_listings_2019-11-09 04_16_comma_separated.csv', sep=',', header=0)

# make column names lower case
column_names = list(df.columns)
column_names = [str(x.lower()) if type(x) is str else x for x in column_names]
df.columns = column_names

df.to_pickle("scientific_plant_names_appendix_I")

#for i in range(len(df.index)):
#    if df.iloc[i,0] == 25968:
#        print(df.iloc[i,9])
