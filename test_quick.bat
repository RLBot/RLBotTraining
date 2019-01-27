@echo off
rem Runs all tests which take barely any time.
rem i.e. They don't require Rocket League.
python -m unittest --verbose tests.metrics tests.grading
