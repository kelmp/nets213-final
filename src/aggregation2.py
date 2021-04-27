from common import read_answers


answer_df = read_answers('../data/sampleAggregationInput.csv', 'Answer.answer')
answer_df.to_csv("../data/sampleAggregationOutput.csv", index=False, quotechar="`")
print(answer_df)
counts = answer_df.groupby('Answer.answer').size()
print(counts)
