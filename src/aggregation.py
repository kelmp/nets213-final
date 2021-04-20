from typing import List, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass


def lists_to_tuples(lists: List[List[str]]) -> Tuple[Tuple[str]]:
    return tuple(tuple(sorted(inner_list)) for inner_list in lists)


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


c1 = Entity(tagged=lists_to_tuples([['Rubis']]))
c2 = Entity(tagged=lists_to_tuples([['Rubis']]))
t1 = Entity(tagged=lists_to_tuples([['Lavander']]))
t2 = Entity(tagged=lists_to_tuples([['Lavander']]))
f1 = Entity(tagged=lists_to_tuples([['Bardic'], ['Inspiration']]))
f2 = Entity(tagged=lists_to_tuples([['Bardic'], ['Inspiration']]))


action = Action(creature=c1, target=t1, feature=f1)
action2 = Action(creature=c2, target=t2, feature=f2)


s = pd.DataFrame(np.array([[action], [action2]]), columns=['action'])
counts = s.groupby('action')
print(counts.size())
