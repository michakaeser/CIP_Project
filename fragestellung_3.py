################################# FRAGESTELLUNG 3 #################################
# In welcher Dekade wurden auf welchem Kontinent die meisten Sportgrossanlässe (Sommer- und Winterolympiade,
# Fussballweltmeisterschaft) durchgeführt?



# Benötigte Libraries laden
import pandas as pd

# Datenquellen werden gelesen
df_wm = pd.read_csv('b1_wm_stage.csv', header=0, encoding='utf-8')
df_wo = pd.read_csv('b2_wolympics_stage.csv', header=0, encoding='utf-8')
df_so = pd.read_csv('b3_solympics_stage.csv', header=0, encoding='utf-8')
df_lc = pd.read_csv('c2_laendercode_stage.csv', header=0, encoding='utf-8')
df_ln = pd.read_csv('c1_country_stage.csv', header=0, encoding='utf-8')

# Der Outputname des Excels definiert
xlsx_output_name = 'Result_Question_03.xlsx'

# Erste Inspektion der Daten
df_wm.info()
df_wo.info()
df_so.info()
df_lc.info()
df_ln.info()

# Aufbereitung Länderkürzel-Dataset
df_lc_new = df_lc.rename(columns={'ISO-3': 'Land_code'})

# Aufbereitung des Datasets Fussballweltmeisterschaften (Neuanordnung der Spalten und Ergänzung um Typ Anlass)
df_wm_new = df_wm[['Jahr', 'Land']]
df_wm_new['Anlass'] = 'Fussballweltmeisterschaft'

# Aufbereitung des Datasets Olympische Sommerspiele (Join mit Ländercode und Neuanordnung der Spalten)
df_so_new = pd.merge(df_so, df_lc_new, on='Land_code', how='inner')
df_so_new.pop('Land_code')
df_so_new = df_so_new[['Jahr', 'Land', 'Anlass']]

# Aufbereitung des Datasets Olympische Winterspiele (Join mit Ländercode und Neuanordnung der Spalten)
df_wo_new = pd.merge(df_wo, df_lc_new, on='Land_code', how='inner')
df_wo_new.pop('Land_code')
df_wo_new = df_wo_new[['Jahr', 'Land', 'Anlass']]

# Zusammenführen der drei Datasets Sportanlässe und anreichern mit Kontinent via inner join auf 'Land' und sortieren
df_events = pd.concat([df_wo_new, df_so_new, df_wm_new])
df_events = pd.merge(df_events, df_ln, on='Land', how='inner')

# Neue Kolonne 'Dekade' wird erstellt, dafür die bestehenden Jahrzahlen kopiert und angepasst
df_events['Dekade'] = df_events['Jahr'].astype('str').str[:3] + '0'
df_events['Dekade'] = df_events['Dekade'].astype('int64')

# Kolonnen werden neu gruppiert und die Zeilen nach dem Jahr sortiert
df_events = df_events[['Jahr', 'Dekade', 'Land', 'Kontinent', 'Anlass']]
df_events = df_events.sort_values(by=['Jahr'], ignore_index=True)

# Finales DataFrame, für welches nichtbenötigte Kolonnen gedroppt werden
df_final = df_events
to_drop = ['Jahr',
           'Land']
df_final.drop(to_drop, inplace=True, axis=1)

# Danach werden die Values pro Dekade und Kontinent gezählt, die Kolonne umbenennt und nach Häufigkeit (Count) sortiert
df_final = df_final.groupby(["Dekade", "Kontinent"], as_index=False).count()
df_final = df_final.rename(columns={'Anlass': 'Anzahl Anlässe'})
df_final = df_final.sort_values(by=['Anzahl Anlässe'], ignore_index=True, ascending=False)

# Schlussendlich wird die Auswertung in ein Excelfile geschrieben
df_final.to_excel(xlsx_output_name, index=False)

#### LESSONS LEARNED ####
# Es ist sehr wichtig, dass gleich zu Beginn des Scraping definiert ist, wie die exportierten und aufbereiteten Daten
# aussehen sollen. So hätte ich mir einige Arbeitsschritte ersparen können, wenn der Teamkollege und ich bereits
# von Anfang an das gleiche Schema verfolgt hätten. So benötigte es meinerseits einige Aufbereitungsschritte mehr,
# die eigentlich bereits im Cleaning-Step erfolgt hätte können.
# GitHub mit der zentralisierten Repository und der Version Control hat uns sehr geholfen, jederzeit "Herr" unserer
# Daten und des Codes zu sein.