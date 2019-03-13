"""dev_server.py
Dynamically renders all pages before serving them.
This is meant to be started via `rlbottraining dev_server <history_dir>`
such that the source code is reloaded when it changes

Usage:
  dev_server.py <history_dir> <host> <port>
  dev_server.py (-h | --help)
  dev_server.py --version

Options:
  -H --history_dir=<path>  Where to persist results of the exercises.
  -h --help                Show this screen.
  --version                Show version.
"""

from pathlib import Path
from http.server import ThreadingHTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

from docopt import docopt

from rlbot.utils.logging_utils import get_logger
from rlbottraining.history.website.authoritative_data_monitor import monitor_authoritative_data
from rlbottraining.history.website.server import Server
from rlbottraining.paths import HistoryPaths
from rlbottraining.version import __version__


def run_devserver(history_dir: Path, host: str, port: int):
    logger = get_logger('dev_server')

    server = None
    def reset_server():
        nonlocal server
        logger.info('Starting server...')
        server = Server(history_dir)
        server.clean_website()
    reset_server()

    serve_dir = history_dir / HistoryPaths.Website._website_dir
    class DevServer(SimpleHTTPRequestHandler):
        def do_GET(self):
            path = Path(self.translate_path(self.path)).relative_to(serve_dir)
            if path == Path('.'):
                path = Path('index.html')
            if path not in server.url_map:
                self.send_error(404)
            server.render_to_disk(path)
            super().do_GET()
        def log_request(self, code='-', size=None):
            logger.info(f'"{self.requestline}" {code} {size if size is not None else ""}')

    handler_class = partial(DevServer, directory=str(serve_dir))

    with monitor_authoritative_data(history_dir, server.add_exercise_result, reset_server):
        with ThreadingHTTPServer((host, port), handler_class) as httpd:
            sa = httpd.socket.getsockname()
            host, port = sa[0], sa[1]
            logger.info(f'Serving HTTP on {host} port {port} (http://{host}:{port}/) ...')
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
    server.clean_website()  # Don't use the partially rendered site for anything.


def main():
    arguments = docopt(__doc__, version=__version__)

    run_devserver(
        history_dir=Path(arguments['<history_dir>']),
        host=arguments['<host>'],
        port=int(arguments['<port>']),
    )

if __name__ == '__main__':
  main()
