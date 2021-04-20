import pandas as pd
import json
from common import read_answers


answer_df = read_answers('sampleAggregationCsv.csv', 'Answer.answer')
print(answer_df)
counts = answer_df.groupby('Answer.answer').size()
print(counts)
