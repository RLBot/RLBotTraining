from typing import Dict
from pathlib import Path
from dataclasses import dataclass

from rlbottraining.history.website.view import Aggregator, Renderer


html_template = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" type="text/css" href="css/main.css" />
  <title>RLBotTraining Site Map</title>
</head>
<body>
<h1>RLBotTraining Site Map:</h1>

{}

</body>
</html>
'''

@dataclass
class SiteMapRenderer(Renderer):
    shared_url_map: Dict[Path, Renderer]

    def render(self) -> str:
        html_body = '\n'.join([
            '<div><a href="{path}">{path}</a></div>'.format(path=str(path))
            for path in self.shared_url_map if path.name.endswith('.html')
        ])
        return html_template.format(html_body)

class SiteMapAggregator(Aggregator):
    """
    Doesn't aggregate results at all, just adds renderers at creation time.
    These renderes just produce the content in the static files contained in static_root.
    """

    serve_path = Path('index.html')
    def __init__(self, shared_url_map: Dict[Path, Renderer]):
        super().__init__(shared_url_map)
        self.shared_url_map[self.serve_path] = SiteMapRenderer(shared_url_map=shared_url_map)
