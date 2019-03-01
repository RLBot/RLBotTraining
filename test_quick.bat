@echo off
rem Runs all tests which take barely any time.
rem i.e. They don't require Rocket League.
python -m unittest --verbose ^
tests.test_metrics ^
tests.test_grading ^
tests.test_dataclasses ^
tests.test_run_module_stubbed ^
