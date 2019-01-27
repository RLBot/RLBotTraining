@echo off
cmd /c "cd tests && python -m unittest discover tests -p *.py --verbose"
