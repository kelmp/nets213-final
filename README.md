# nets213-final

## Major Components

Let's overview the major components in this project.

### MTurk Crowdsourcing

This is how we will annotation our training data. The worker will tag relevant
things from the sentence, namely: who is the object, who is the target, what
kind of action are they performing? Our current HIT design is in
`src/DnD-HIT.html`.

### Quality Control

We will use an embedded Gold Standard in our MTurk HITs. The worker's
performance on these Gold Standard examples is used as a weight to compute the
majority vote using weighted averages. Our current rough implementation is in
`src/qc.py`.

### Aggregation

In order to train the model we need to during all of the MTurk data into a CSV
that can be read into the model. We also need to ensure there are no duplicates,
sentences are correctly structured, and may possibly perform NLP operations to
sanitize the data. Our current rough implementation is in `src/aggregation2.py`.

### Trained Model

This is the actual model we are training with the aggregated data. The model
will take in a plain text sentence and attempt to perform the same annotation
process as the MTurk workers did previously. That is to say, it should identify
the object of the sentence, target of an action, and the action being performed.
These files will be in `ml-parser`.

### User-Facing Application

Web application with a simple input and output text box. When the user types in
a plain text sentence, we run it through the trained model to get annotations.
Then, we send the annotated sentence through Avrae Command Generator API which,
when provided the object, target, and action, will be able to generate a valid
Dungeons & Dragons command. This valid command is then displayed to the users in
the output text box.

### Avrae Command Generator

The [Avrae Command Generator](https://avrae.io/) is a deterministic program
which provides an API we can use to turn the users annotated sentence into a
valid Dungeons & Dragons command. With this command, based on the user's
free-form plain text input which has been annotated by our trained model, we can
return a command corresponding to their sentence.

## Rubric

We have come up with the following rubric for our project:

- [ ] HIT Design
  - [4] HIT only allows users to select whole words; accessible keybindings for
    adding additional actions and switching tags
  - [3] HIT only allows users to select whole words; users can add actions and
    switch between tags with mouse
  - [2] HIT allows users to select arbitrary text to categorize
  - [1] HIT design is not representative of the project
- [ ] Quality Control
  - [4] Tags are mostly correct
  - [3] Tags are generally correct
  - [2] Tags are generally incorrect
  - [1] Tags are mostly incorrect
- [ ] Model
  - [4] Model can take in arbitrary descriptive text and returns generally
    accurate categorized data for described actions
  - [3] Model finds described actions, but has difficulties matching actions to
    relevant entities or targets
  - [2] Model finds described actions, but tends to tag part of the token or
    more than the necessary token
  - [1] Model does not satisfactorily find described actions
- [ ] User-Facing Application
  - [4] Intuitive interface that properly handles user input, sends the input
    through our model, routes the model’s output through the Avrae command
    generator API, and displays the response command from Avrae.
  - [3] Unintuitive interface that properly handles user input, sends the input
    through our model, routes the model’s output through the Avrae command
    generator API, and displays the response command from Avrae.
  - [2] Unintuitive interface that handles user input, sends the input through
    our model, routes the model’s output through the Avrae command generator
    API, and displays the response command from Avrae, but sometimes fails or
    faults resulting in the user not receiving the response.
  - [1] Unintuitive interface that never correctly responds with the proper
    output.

## Important Files

- `docsFlowDiagram.png` - Flow diagram modeling the interaction between our
  modules
- `docs/HIT mockup.png` - mockup of our HIT design
- `docs/User Application mock-up.png` - mockup of our user application
- `data/phandelever-labels.json` - our raw data
- `data/sampleAggregationInput.csv` - sample input to aggregation module
- `data/sampleAggregationOutput.csv` - sample output from aggregation module
- `data/qcInput.csv` - sample input to quality control module
- `data/qcOutput.csv` - sample output from quality control module
- `src/aggregation2.py` - our current implementation of aggregation, centering
  around messy use of JSON strings
- `src/qc.py` - our current implementation of quality control, which uses gold
  standard accuracies to vote on correct actions
- `src/DnD-HIT.html` - our current implementation of the MTurk HIT

## Code Documentation

- HIT: Users select one or more words with the mouse, then use buttons or hotkeys to tag them as a single entity with a corresponding tag. Once all entities for a single action are tagged, the user can click "Done with this action" and move on to another action in the same text sample. If there are no more actions in the current text sample, the user can click "Finished with this block of text" to submit all of their tags.
- QC: Gold standard answers are used to compute F1 scores for each worker. After that, weighted majority voting is used to determine which of the answers submitted by workers are "correct." An answer is accepted if the average F1 score of the workers who listed it as an answer is at least as high as the average F1 score across all workers.
- Aggregation:
The answer_to_hashable method in common.py converts the object resulting from a json.loads() call into a form suitable
  for the DataFrame.explode(). It takes in the actions parameter, where the outermost list is the list of actions submitted by a
  single worker. The dict maps a single action's tags to a list of phrases with that tag for this action.
  This returns a list of JSON strings, so that when explode() is called, each row contains the JSON for a single action with 
  keys sorted alphabetically.
A dataframe is produced from which a groupby can be run based on the 'Answer.answer' column containing the labels provided by the responder, 
  which we can use to train a classifier.
- Analysis - We plan to collect data from both Turkers and DnD experts (in the form of friends) to train the model on two sets of data. We will then conduct an analysis on the performance differences between the two demographics

## HIT Instructions
1. Familiarize yourself with the categories listed below the text. 
2. Read the text. 
3. For each action in the text, complete Steps 4 and 5. 
4. Click all words that you think belong in the same category (they will be highlighted a certain color), then select a category using either mouse or key inputs. 
5. Repeat Step 4 for each of the categories you wish to label in the action. 

Note: You can assign multiple categories to a single word or group of words. 

