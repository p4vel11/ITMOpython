from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from models import Author, App, User, UserCurrency
from utils.currencies_api import get_currencies
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

template_dir = os.path.join(os.path.dirname(__file__), "templates")

env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape()
)

main_author = Author(name="Солдатов Павел", group="Группа-3123")
my_app = App(name="Лабораторная работа 8", version="888", author=main_author)

users = [
    User(id_=1, name="Виктор"),
    User(id_=2, name="Марина")
]

user_subscriptions = {
    1: ["R01235", "R01239"],
    2: ["R01235"]
}

cached_currencies = get_currencies()
currency_map = {c.id: c for c in cached_currencies}

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        route = parsed_path.path
        query = parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        if route == "/":
            template = env.get_template("index.html")
            html = template.render(app=my_app)
        elif route == "/author":
            template = env.get_template("user.html")
            html = template.render(app=my_app)
        elif route == "/users":
            template = env.get_template("users.html")
            html = template.render(users=users)
        elif route == "/user":
            user_id = int(query.get("id", [0])[0])
            user = next((u for u in users if u.id == user_id), None)
            if user:
                subscribed_currencies = [
                    currency_map[cid] for cid in user_subscriptions.get(user_id, [])
                    if cid in currency_map
                ]
                template = env.get_template("user.html")
                html = template.render(user=user, currencies=subscribed_currencies)
            else:
                html = "<h1>Пользователь не найден</h1>"
        elif route == "/currencies":
            currencies = get_currencies()
            template = env.get_template("currencies.html")
            html = template.render(currencies=currencies)
        else:
            self.send_response(404)
            html = "<h1>404 Not Found</h1>"

        self.wfile.write(html.encode("utf-8"))

def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()