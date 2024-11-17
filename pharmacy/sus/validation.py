import pandas as pd


data = pd.read_csv('file.csv')

data = data[data['name'] != '""']
data['name'] = data['name'].str.strip()
data = data.dropna(how='all')

data.to_csv('file.csv', index=False)
