# RLBotTraining
Customizable training for Rocket Leage bots of any language.


## Instalation

 - Clone this repo (`RLBot/RLBotTraining`)
 - TODO(This step will be unnecessary once the branch is merged): Use the `RLBotTraining` branch of `RLBot/RLBot`)
 - `python run_exercises.py`


## Architecture

 - At the entry point (`run_exercises.py`) we decide which `GraderExercise` should be run and the `config_path`s define the RLBot setup to be used (which bots, which mode).
 - Each `GraderExercise` composes together the initial game state and how the bot is judged. The responsibility of judging the bot is handled by `Grader`s
 - A `Grader` decides whether to continue the exercise or to `Pass`/`Fail` the exercise by looking at each tick. A `Grader` may optionally gather metrics (e.g. "time until goal") to help track bot performance as the bot is improved.
 - Separation of responsiblity: This repository is designed to make it nice to define new exercises whereas the training API of the `RLBot` framework provides the minimum features for any training to occur.


## Tips for writing your own exercises:

 - Always subclass `GraderExercise` rather than `Exercise`. Using `Grader`s will allows you to share termination conditions, safely store state across ticks and provide metrics.
 - Compose your `Grader`s. For instance, by using `CompoundGrader`
 - Provide meaningful error messages in your `Grader`s by subclassing `Fail`


## Future direction

 - Provide playlists
 - Provide an example of striker vs goalie
 - Allow imports from RocketLeague Training
 - Put metrics (`Grader.get_metrics()`) into a database
 - A way of browsing past runs, including metrics
 - Reproducing failed exercises
 - Visualization of metrics
 - Continous integration of different bots
