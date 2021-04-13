# nets213-final

## Major Components

Let's overview the major components in this project.

### MTurk Crowdsourcing

This is how we will annotation our training data. The worker will tag relevant things from the sentence, namely: who is the object, who is the target, what kind of action are they performing?

### Quality Control

We will use an embedded Gold Standard in our MTurk HITs. The worker's performance on these Gold Standard examples is used as a weight to compute the majority vote using weighted averages.

### Aggregation

In order to train the model we need to during all of the MTurk data into a CSV that can be read into the model. We also need to ensure there are no duplicates, sentences are correctly structured, and may possibly perform NLP operations to sanitize the data.

### Trained Model

This is the actual model we are training with the aggregated data. The model will take in a plain text sentence and attempt to perform the same annotation process as the MTurk workers did previously. That is to say, it should identify the object of the sentence, target of an action, and the action being performed.

### User-Facing Application

Web application with a simple input and output text box. When the user types in a plain text sentence, we run it through the trained model to get annotations. Then, we send the annotated sentence through Avrae Command Generator API which, when provided the object, target, and action, will be able to generate a valid Dungeons & Dragons command. This valid command is then displayed to the users in the output text box.

### Avrae Command Generator

The [Avrae Command Generator](https://avrae.io/) is a deterministic program which provides an API we can use to turn the users annotated sentence into a valid Dungeons & Dragons command. With this command, based on the user's free-form plain text input which has been annotated by our trained model, we can return a command corresponding to their sentence.

## Rubric

We have come up with the following rubric for our project:

- [ ] HIT Design
    - [4] HIT only allows users to select whole words; accessible keybindings for adding additional actions and switching tags
    - [3] HIT only allows users to select whole words; users can add actions and switch between tags with mouse
    - [2] HIT allows users to select arbitrary text to categorize
    - [1] HIT design is not representative of the project
- [ ] Quality Control
    - [4] Tags are mostly correct
    - [3] Tags are generally correct
    - [2] Tags are generally incorrect
    - [1] Tags are mostly incorrect
- [ ] Model
    - [4] Model can take in arbitrary descriptive text and returns generally accurate categorized data for described actions
    - [3] Model finds described actions, but has difficulties matching actions to relevant entities or targets
    - [2] Model finds described actions, but tends to tag part of the token or more than the necessary token
    - [1] Model does not satisfactorily find described actions
- [ ] User-Facing Application
    - [4] Intuitive interface that properly handles user input, sends the input through our model, routes the model’s output through the Avrae command generator API, and displays the response command from Avrae.
    - [3] Unintuitive interface that properly handles user input, sends the input through our model, routes the model’s output through the Avrae command generator API, and displays the response command from Avrae.
    - [2] Unintuitive interface that handles user input, sends the input through our model, routes the model’s output through the Avrae command generator API, and displays the response command from Avrae, but sometimes fails or faults resulting in the user not receiving the response.
    - [1] Unintuitive interface that never correctly responds with the proper output.

