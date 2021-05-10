import pandas as pd


def reformat(df):
    return df.drop(columns='WorkerId').rename(
        columns={'Input.prompt': 'input', 'Answer.answer': 'tags'})


friend_and_gold = pd.read_csv('../public-hit/trimmed_public.csv', quotechar='`')
friend_and_gold = reformat(friend_and_gold)
friend_and_gold.to_csv('../data/trainingData/friend_and_gold.csv', index=False)

gold = pd.read_csv('../data/goldStandard/goldAnswers.csv', quotechar='`')
gold = reformat(gold)
mturk = pd.read_csv('../training-data-processor/mturk_labels.csv')
mturk_and_gold = pd.concat((gold, mturk))
mturk_and_gold.to_csv('../data/trainingData/mturk_and_gold.csv', index=False)
