import csv

import pandas as pd


answers = pd.read_csv('../data/goldStandard/goldAnswers.csv', quotechar='`')
prompts = answers['Input.prompt'].rename('prompt')
replaced = prompts.str.replace(pat='"', repl="'")
print(replaced)
replaced.to_csv('../data/goldStandard/goldPromptsSingleQuote.csv',
                index=False)
# prompts.to_csv('../data/goldPrompts.csv', quotechar='`', index=False)
# print(answers)
