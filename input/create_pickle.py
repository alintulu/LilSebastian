import pandas as pd

df = pd.read_csv('cites_listings_2019-11-09 04_16_comma_separated.csv', dtype=str, sep=',',header=0)

# make column names lower case
column_names = list(df.columns)
column_names = [x.lower() if type(x) is str else x for x in column_names]

df.columns = column_names

df.to_pickle("scientific_plant_names_appendix_I")


