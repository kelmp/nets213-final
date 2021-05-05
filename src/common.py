from typing import List, Dict

import pandas as pd
import json


def answer_to_hashable(actions: List[Dict[str, Dict[str, List[List[str]]]]]) \
        -> List[str]:
    """
    NOTE: THIS ONLY WORKS WITH THE NEW SCHEMA! Old sample data that didn't
    include indices will *not* work with this.
    
    Converts the object resulting from a json.loads() call into a form suitable
    for DataFrame.explode().
    :param actions:
        Outermost list is a worker's list of actions for a text sample.
        Each action is a dict mapping tags to a dict with two keys:
            "words" and "indices".
        "words" maps to a list of list of strings (an inner list is an entity)
        "indices" maps to a list of list of ints
    :return: A list of JSON strings, such that when explode() is called,
             each row contains the JSON for a single action. Keys should be
             sorted alphabetically.
    """
    # The output itself is not hashable, but the tuples within it
    # (which represent individual actions) are.
    for a_dict in actions:
        for tag in a_dict:
            a_dict[tag] = sorted(a_dict[tag]['words'])
    return [json.dumps(a_dict, sort_keys=True) for a_dict in actions]


def read_answers(path: str, answer_col: str) -> pd.DataFrame:
    df = pd.read_csv(path, quotechar='`', converters={answer_col: json.loads})
    df[answer_col] = df[answer_col].map(answer_to_hashable)
    return df.explode(answer_col)
