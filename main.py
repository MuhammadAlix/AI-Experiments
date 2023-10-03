import pandas as pd
from chembl_webresource_client.new_client import new_client
import csv

target = new_client.target
target_query = target.search('CHEMBL4315')
targets = pd.DataFrame.from_dict(target_query)
# print(targets)

selected_target = targets.target_chembl_id[0]
print(selected_target)

activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")
df = pd.DataFrame.from_dict(res)
# print(df)

# print(df.head(4))

# print(df.standard_type.unique())

df.to_csv('P2Y1-01-bioactivity_data_raw.csv', index=False)

df2 = df[df.standard_value.notna()]
df2 = df[df.canonical_smiles.notna()]
# print(df2)
len(df2.canonical_smiles.unique())
df2_nr = df2.drop_duplicates(['canonical_smiles'])
# print(df2_nr)
selection = ['molecule_chembl_id','canonical_smiles','standard_value']
df3 = df2_nr[selection]
# print(df3)

df3.to_csv('P2Y1-bioactivity-data-02-preprocessed.csv', index=False)

df4 = pd.read_csv('P2Y1-bioactivity-data-02-preprocessed.csv')

bioactivity_threshold = []
for i in df4.standard_value:
  if float(i) >= 10000:
    bioactivity_threshold.append("inactive")
  elif float(i) <= 1000:
    bioactivity_threshold.append("active")
  else:
    bioactivity_threshold.append("intermediate")

bioactivity_class = pd.Series(bioactivity_threshold, name='class')
df5 = pd.concat([df4, bioactivity_class], axis=1)
# print(df5)

df5.to_csv('P2Y1_03_bioactivity_data_curated.csv', index=False)