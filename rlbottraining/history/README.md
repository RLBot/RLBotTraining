# Usual use of the RLBotTraining metrics architecture.
## Written as a story about a fictional bot-maker "Taylor".

- Taylor creates a bot in a programming language of their choosing.
- Taylor makes RLBotTraining GraderExercise's for the bot and also runs some of the Exercises contained in RLBotTraining as well.
- These Exercises use include a Grader which could be from the framework or Taylor could write a Grader which is only applicable to their bot to train some special task.
- TODO: When an exercise finishes, grader.get_metric() is called.
- TODO: These metrics are wrapped with information to reproduce the exercise and written to disk in JSON format within a `metrics_dir` of Taylors choosing.
- TODO: The rlbottraining.metrics.viewer submodule helps us make sense of the metrics in the `metrics_dir`.
- TODO: Its purpose is to create views on the metrics_dir which manifests itself as generating a website hosting a static view of the data.
- TODO: Having a static website makes hosting/sharing/viewing the results easy:
- TODO: For instance, Taylor can push this static website to https://pages.github.com/ or host it locally using the built-in `python -m http.server`.
- TODO: The website generation automatically generates a bunch of useful "View-Data" JSON files to support aggregations of the metrics
- TODO: An example of an aggregation would be "Winrate of TaylorBot vs NomBot".
- TODO: The generated website includes JS to to allow visualizations of the View Data.
- TODO: Taylor may add their own visualization and additions to View Data by providing WebsiteExtension's when generating the website.
- TODO: Taylor now can view nicely visualizied, aggregated results generated for their bot training and share this with others.
- TODO: Taylor now can re-run exercises which had an odd outcome to debug problems in the bot.
