import pandas as pd
from common import read_answers


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', None)


def compute_gold_f1(gold_path: str, gold_answer_col: str, agg_out_path: str) \
        -> pd.Series:
    gold = read_answers(gold_path, gold_answer_col)
    agg_out = pd.read_csv(agg_out_path, quotechar='`')

    # number of actions in the gold standard for each prompt
    gold_num_correct = gold.groupby("prompt").size().to_frame("gold_correct")

    compare = gold.merge(agg_out, left_on="prompt", right_on="Input.prompt")
    compare["correct"] = compare["Answer.answer"] == compare["gold_answer"]

    # number of correct actions found by each worker on each prompt
    correct_per_prompt = compare[compare["correct"]].groupby(
        ["WorkerId", "prompt"]).size().to_frame("true_pos").reset_index()
    correct_per_prompt["answered"] = agg_out.groupby(
        ["WorkerId", "Input.prompt"]).size().to_frame(
        "answered").reset_index()["answered"]

    # find proportion of gold standard correct over all prompts
    correct_all_prompts = gold_num_correct.merge(correct_per_prompt, on="prompt")
    prompt_acc = correct_all_prompts.groupby(["WorkerId", "prompt"]).sum()
    prompt_acc["false_pos"] = prompt_acc["answered"] - prompt_acc["true_pos"]
    prompt_acc["false_neg"] = prompt_acc["gold_correct"] - prompt_acc["true_pos"]
    prompt_acc["f1"] = prompt_acc["true_pos"] / (
        prompt_acc["true_pos"] + .5 * (prompt_acc["false_pos"] +
                                       prompt_acc["false_neg"]))
    return prompt_acc.groupby("WorkerId").mean()["f1"].reset_index()


def gold_weighted_vote(gold_f1s: pd.Series, agg_out_path: str) \
        -> pd.DataFrame:
    """
    Finds the majority vote answers after gold-standard weighting. A particular
    answer configuration must get at least 50% of the total F1 score in order
    to be counted as "correct."

    This isn't perfect since it doesn't
    differentiate between a missed answer and an intentionally omitted answer -
    it just assumes that missing answers are intentionally omitted. It also
    has no way of determining when answers are conflicting.
    Possible TODO for later: try to determine equivalence? Reintroducing
             dataclasses could help in order to set the criteria that denote
             tagged actions that are targeting the same thing...but that's
             getting into the realm of NER (I think?)
    :param gold_f1s: Workers' gold standard F1 scores from compute_gold_f1
    :param agg_out_path: Path to the result of running aggregation processes
                         on the data we need votes on (to explode action lists)
    :return: The actions that received >= 50% of the total f-score
    """
    majority = gold_f1s["f1"].mean(axis=0)
    agg_out = pd.read_csv(agg_out_path, quotechar='`')
    scored = agg_out.merge(gold_f1s, on="WorkerId").groupby(
        ["Input.prompt", "Answer.answer"]).mean().drop(columns=["WorkerId"])
    valid = scored[scored["f1"] >= majority].reset_index().drop(columns=["f1"])
    return valid


f1s = compute_gold_f1("../data/sampleGoldCsv.csv", "gold_answer",
                      "../data/sampleAggregationOutput.csv")
print(f1s)
vote_answers = gold_weighted_vote(f1s, "../data/qcInput.csv")
print(vote_answers)
vote_answers.to_csv("../data/qcOutput.csv", quotechar="`", index=False)
