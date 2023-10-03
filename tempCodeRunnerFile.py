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
print(df)