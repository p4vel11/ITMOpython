from jinja2 import Environment, FileSystemLoader
import os

class PageRenderer:
    def __init__(self, template_dir="templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render(self, template_name: str, context: dict = None):
        if context is None:
            context = {}
        template = self.env.get_template(template_name)
        return template.render(**context)