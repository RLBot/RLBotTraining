"""RLBotTraining
Runs the training exercise playlist in the given python file.
The playlist has to be provided via a make_default_playlist() function.

Usage:
  rlbottraining run_module <python_file> [--history_dir=<path>]
  rlbottraining history_dev_server <history_dir> [--host=<host>] [--port=<port>]
  rlbottraining history_render_static <history_dir>
  rlbottraining (-h | --help)
  rlbottraining --version

Options:
  -H --history_dir=<path>  Where to persist results of the exercises.
  --host=<host>            [default: localhost].
  --port=<port>            [default: 8000]
  -h --help                Show this screen.
  --version                Show version.
"""

from pathlib import Path

from docopt import docopt

from rlbottraining.version import __version__
from rlbottraining.exercise_runner import run_module
from rlbottraining.history.website.server import Server
from rlbottraining.history.website.dev_server_restarter import restart_devserver_on_source_change

def main():
    arguments = docopt(__doc__, version=__version__)
    if arguments['run_module']:
        run_module(
            Path(arguments['<python_file>']),
            history_dir=arguments['--history_dir']
        )
    if arguments['history_render_static']:
        server = Server(history_dir=Path(arguments['<history_dir>']))
        server.render_static_website()
    elif arguments['history_dev_server']:
        restart_devserver_on_source_change(
            arguments['<history_dir>'],
            arguments['--host'],
            arguments['--port'],
        )

if __name__ == '__main__':
  main()
