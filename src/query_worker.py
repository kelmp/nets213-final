import pandas as pd
from json import loads

id_stub = 'A3UUH363'

df = pd.read_csv('../data/responses/earlyGold.csv')
from_worker = df[df['WorkerId'].str.startswith('A3UUH363')]
worker_prompt = from_worker['Input.prompt'].tolist()
worker_ans = from_worker['Answer.tags'].tolist()
response = loads(worker_ans[0])

print(worker_prompt)
print(response)
