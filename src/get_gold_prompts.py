import pandas as pd


answers = pd.read_csv('../data/goldAnswers.csv', quotechar='`')
prompts = answers['Input.prompt'].rename('prompt')
print(prompts)
prompts.to_csv('../data/goldPrompts.csv', quotechar='`', index=False)
# print(answers)
