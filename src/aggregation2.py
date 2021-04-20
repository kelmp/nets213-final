from typing import List, Dict
import pandas as pd
import json


def answer_to_hashable(actions: List[Dict[str, List[List[str]]]]) -> List[str]:
    """
    Converts the object resulting from a json.loads() call into a form suitable
    for DataFrame.explode().
    :param actions: Outermost list is the list of actions submitted by a
                    single worker. The dict maps a single action's tags to
                    a list of phrases with that tag for this action.
                    Each phrase is a list made up of individual words.
    :return: A list of JSON strings, such that when explode() is called,
             each row contains the JSON for a single action. Keys should be
             sorted alphabetically.
    """
    # The output itself is not hashable, but the tuples within it
    # (which represent individual actions) are.
    out = []
    for a_dict in actions:
        for tag in a_dict:
            a_dict[tag] = sorted(a_dict[tag])
    return [json.dumps(a_dict, sort_keys=True) for a_dict in actions]


df = pd.read_csv('sampleAggregationCsv.csv', quotechar='`',
                 converters={'Answer.answer': json.loads})
print(df)

df['Answer.answer'] = df['Answer.answer'].map(answer_to_hashable)
exploded = df.explode('Answer.answer')
print(exploded)

counts = exploded.groupby('Answer.answer').size()
print(counts)
