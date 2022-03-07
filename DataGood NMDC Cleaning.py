import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy
from pathlib import Path
import re
import nltk
import string

plt.style.use('fivethirtyeight')
sns.set()
sns.set_context("talk")

# Setup - Load the SQL extension and connect to the Mini IMDB dataset we've prepared
db_path = Path('/Users/ryan/Downloads/biosample_basex_data_good_subset.db')

engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
connection = engine.connect()
inspector = sqlalchemy.inspect(engine)

query_name = """
SELECT *
FROM harmonized_wide_sel_envs
"""
df = pd.read_sql(query_name, engine)

df['rel_to_oxygen_rep'] = df['rel_to_oxygen'].astype(str).astype('string')
df['rel_to_oxygen_status'] = "None"
arr = df['rel_to_oxygen_rep'].values
ps = nltk.PorterStemmer()
df['rel_to_oxygen_rep'] = [ps.stem(word) for word in arr]
comparison = df['rel_to_oxygen_rep'].copy()

df['rel_to_oxygen_rep'] = df['rel_to_oxygen_rep'].replace(to_replace = ["obligate anaerob", "facultative anaerob", "anaerob", "facultative anaerob"], value="anaerobe")
df['rel_to_oxygen_rep'] = df['rel_to_oxygen_rep'].replace(to_replace = ["aerob"], value="aerobe")
#replacing NaN values with "repair" for the words just replaced
df['rel_to_oxygen_status'] = df['rel_to_oxygen_status'].where(comparison == df['rel_to_oxygen_rep'], 'Repaired')

bool_list = df['rel_to_oxygen_rep'].str.contains('mg\/l$', regex = True)
#df['rel_to_oxygen_status'] = df['rel_to_oxygen_status'].where(comparison == df['rel_to_oxygen'], "Couldn't Repair")
df['rel_to_oxygen_rep'] = df['rel_to_oxygen_rep'].where(bool_list == False, None)
df['rel_to_oxygen_rep'] = df['rel_to_oxygen_rep'].where(df['rel_to_oxygen_rep'] != 'none', None)

df['rel_to_oxygen_rep'] = df['rel_to_oxygen_rep'].replace(to_replace = ['oblig', 'oxic', 'hypox', 'aerobic-anaerob', 'oxic/anoxic boundari', 'microaerophil', 'normal oxic seawat', 'facult'], value=None)
filter1 = df['rel_to_oxygen_status']== 'Repaired'
df['rel_to_oxygen_status'] = df['rel_to_oxygen_status'].where(filter1, "Couldn't Repair")

df['air_temp'] = df['air_temp'].str.replace(" degree Celsius", "")
df['air_temp'] = df['air_temp'] + " degree Celsius"


