#### frage 2: Welcher Kontinent verzeichnet den grössten BIP-Zuwachs in der Periode von 2000-2019?
####
#### input: country_stage.csv, länderkode_stage.csv, rgdpna.csv
#### output:
#### process: verbinden von country_stage.csv mit rgdpna.csv via länderkürzel-ländername von länderkode_stage.csv
#### target df laypout: kontinent, ländername, jahr, bip

#load libraries
import pandas as pd
from matplotlib import pyplot as plt

#load data
df_c = pd.read_csv('country_stage.csv', header=0, encoding='utf-8')
df_k = pd.read_csv('länderkode_stage.csv', header=0, encoding='utf-8')
df_r = pd.read_csv('rgdpna.csv', header=0, encoding='utf-8')

#first data inspection
df_c.head()
df_c.info()
df_k.head()
df_k.info()
df_r.head()
df_r.info()

#drop superfluous column
df_r = df_r.drop(columns="VariableCode")

#join all tables together
df_joined_1 = pd.merge(df_c, df_k, on='Land', how='inner')
df_joined_1.head()
df_joined_1.info()

# -> loss of ~ 60 entries after merge. deeper look at "länderkode_stage.csv"...
# revealed that the naming of the country is not consistent at all,...
# thus, a manual review is necessary.
################################################################################################
#### input: länderkode_stage.csv
#### process: manual correction
#### output: länderkode_stage_v2.csv

#find difference - "comparing country_stage" with "länderkode_stage"
for l in df_k['Land']:
    if not df_c['Land'].str.contains(l).any():
        print(l)

df_k = pd.read_csv('länderkode_stage_v2.csv', header=0, encoding='utf-8')
df_k.info()
#-> loss of ~ 20 entries. no impactfull country left out

df_joined_1 = pd.merge(df_c, df_k, on='Land', how='inner')
df_joined_1.head()
df_joined_1.info()
################################################################################################
#go on with merging with new manually corrected csv-file
df_joined_2 = pd.merge(df_joined_1, df_r, left_on='ISO-3', right_on='RegionCode', how='inner')
df_joined_2.head()
df_joined_2.info()

#reindexing the df and group by index, with sum of column value
# - column with none numerical values get lost during process -> which is actually desired
df_i2 = df_joined_2.set_index(['Kontinent', 'YearCode'])
new_df2 = df_i2.groupby(level= ['Kontinent', 'YearCode']).sum()

#reset the index -> indexes become columns
df_res2 = new_df2.reset_index()
df_res2.info()

#first data analyis: gdp-time by continent
df_piv = df_res2.pivot(index='YearCode', columns='Kontinent', values='AggValue')
df_piv.plot()

#######################
#keep only row with year 2000 or 2019
df_j = df_joined_2.drop(df_joined_2[(df_joined_2.YearCode != 2000) & (df_joined_2.YearCode != 2019)].index)
df_j.head()
df_j.info()

#reindexing the df and group by index, with sum of column values
df_i = df_j.set_index(['Kontinent', 'YearCode'])
new_df = df_i.groupby(level= ['Kontinent', 'YearCode']).sum()
#reset the index -> indexes become columns
df_res = new_df.reset_index()

#creation of a function, in order to calculate absolut difference of the GDP's
def delta_gdp(name):
    d = float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2019)]) - \
        float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2000)])
    return d

#creation of a function in order to calculate relative difference of the GDP's
def delta_gdp_r(name):
    d = float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2019)]) / \
        float(df_res['AggValue'][(df_res.Kontinent == name) & (df_res.YearCode == 2000)])
    return d

#new data variables with values from the functions
a = {"Afrika": [delta_gdp("Afrika")],
    "Asien": [delta_gdp("Asien")],
    "Australien": [delta_gdp("Australien")],
    "Europa": [delta_gdp("Europa")],
    "Europa/Asien": [delta_gdp("Europa/Asien")],
    "Nordamerika": [delta_gdp("Nordamerika")],
    "Suedamerika": [delta_gdp("Suedamerika")]
     }
a_df = pd.DataFrame(a)

b = {"Afrika": [delta_gdp_r("Afrika")],
    "Asien": [delta_gdp_r("Asien")],
    "Australien": [delta_gdp_r("Australien")],
    "Europa": [delta_gdp_r("Europa")],
    "Europa/Asien": [delta_gdp_r("Europa/Asien")],
    "Nordamerika": [delta_gdp_r("Nordamerika")],
    "Suedamerika": [delta_gdp_r("Suedamerika")]
     }
b_df = pd.DataFrame(b)

#invert index with column, and sort gdp (ascending)
xx = b_df.T
x1 = xx.sort_values(by=0)
x2 = x1.reset_index()
x2.columns = ["Kontinent", "GDP"]
x2.plot.bar(x='Kontinent', y='GDP', color = "green")
plt.title('relative change of GDP')

yy = a_df.T
y1 = yy.sort_values(by=0)
y2 = y1.reset_index()
y2.columns = ["Kontinent", "GDP"]
y2.plot.bar(x='Kontinent', y='GDP', color = "gold")
plt.title('absolut change of GDP')


#### lessons learned
# - scientific notation (3.45e+08), stored as a text type, can be correctly interpreted in python
#       by converting it into a float number
# - Group by with sum() can drop columns
# - set index with clumns and then reset the index can be powerfull for quick data manupulation