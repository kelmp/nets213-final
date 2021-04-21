from typing import List, Tuple

import pandas as pd
import numpy as np
from dataclasses import dataclass
import json


def lists_to_tuples(lists: List[List[str]]) -> Tuple[Tuple[str]]:
    output = []
    for inner_list in lists:
      if type(inner_list) == list:
         output.append(tuple(tuple(sorted(inner_list))))
      else:
        output.append(inner_list)
    x = tuple(sorted(output))
    return x



@dataclass(eq=True, frozen=True)
class Entity:
    tagged: Tuple[Tuple[str]] = None


@dataclass(eq=True, frozen=True)
class Action:
    creature: Entity = None
    target: Entity = None
    attack: Entity = None
    spell: Entity = None
    feature: Entity = None
    attackRoll: Entity = None
    damageRoll: Entity = None
    savingThrow: Entity = None

    
    #def __hash__(self):
      #return hash(self.creature)

    #def __lt__(self, other):
      #return 

    def __eq__(self, other):
      return self.creature == other.creature and self.target == other.target \
      and self.attack == other.attack and self.spell == other.spell \
      and self.feature == other.feature and self.attackRoll == other.attackRoll \
      and self.damageRoll == other.damageRoll and self.savingThrow == other.savingThrow
    



#data 

class Aggregation:

  def aggregate(filename):
    data = pd.read_csv(filename, names=["workerId", "Input.prompt", "Answer.answer"])
    actions = []

    for i in data.iterrows():
      new_data = eval(i[1][2])
      c: Entity = None
      t: Entity = None
      a: Entity = None
      s: Entity = None
      f: Entity = None
      ar: Entity = None
      d: Entity = None
      st: Entity = None
      for key, value in new_data.items():
        if key == "creature":
          c = Entity(tagged=lists_to_tuples(value))
        elif key == "target":
          t = Entity(tagged=lists_to_tuples(value))
        elif key == "attack":
          a = Entity(tagged=lists_to_tuples(value))
        elif key == "spell":
          s = Entity(tagged=lists_to_tuples(value))
        elif key == "feature":
          f = Entity(tagged=lists_to_tuples(value))
        elif key == "attackRoll":
          ar = Entity(tagged=lists_to_tuples(value))
        elif key == "damageRoll":
          d = Entity(tagged=lists_to_tuples(value))
        elif key == "savingThrow":
          st = Entity(tagged=lists_to_tuples(value))
      action = Action(creature=c, target=t, attack=a, spell=s, feature=f, 
                      attackRoll=ar, damageRoll=d, savingThrow=st)
      actions.append(action)

    data["action"] = actions
    return data


#output = Aggregation.aggregate("mturk_results.csv")
#output.to_csv("output")
#output.groupby("action").head()
