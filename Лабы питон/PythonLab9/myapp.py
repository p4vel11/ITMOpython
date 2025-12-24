from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime

from controllers.databasecontroller import DatabaseConnection, CurrencyRatesCRUD, UserCRUD, UserCurrencyCRUD
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController
from controllers.pages import PageRenderer

db = DatabaseConnection()
currency_db = CurrencyRatesCRUD(db)
user_db = UserCRUD(db)
subscription_db = UserCurrencyCRUD(db)

currency_controller = CurrencyController(currency_db)
user_controller = UserController(user_db, subscription_db)
renderer = PageRenderer()

# Заполнение тестовыми данными
initial_currencies = [
    {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
    {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 91.5, "nominal": 1},
]
for c in initial_currencies:
    currency_db.create(c)

user_db.create("Марина")
user_db.create("Виктор")
# Подписка пользователя 1 на USD и EUR
subscription_db.subscribe(1, 1)
subscription_db.subscribe(1, 2)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        if path == "/":
            html = renderer.render("index.html")
        elif path == "/author":
            html = renderer.render("author.html", {"current_date": datetime.now().strftime("%d.%m.%Y")})
        elif path == "/currencies":
            currencies = currency_controller.list_currencies()
            html = renderer.render("currencies.html", {"currencies": currencies})
        elif path == "/currency/delete":
            currency_id = int(query.get("id", [0])[0])
            currency_controller.delete_currency(currency_id)
            self.send_response(302)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return
        elif path == "/currency/update":
            char_code = next(iter(query))
            value = float(query[char_code][0])
            currency_controller.update_currency(char_code, value)
            self.send_response(302)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return
        elif path == "/users":
            users = user_controller.list_users()
            html = renderer.render("users.html", {"users": users})
        elif path == "/user":
            user_id = int(query.get("id", [0])[0])
            user_info = user_controller.get_user_by_id(user_id)
            if user_info:
                html = renderer.render("user.html", {"user_info": user_info})
            else:
                html = "<h2>Пользователь не найден</h2>"
        elif path == "/currency/show":
            currencies = currency_controller.list_currencies()
            print("Текущие валюты:", json.dumps(currencies, indent=2, ensure_ascii=False))
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Валюты выведены в консоль.".encode('utf-8'))
            return
        else:
            html = "<h2>404 Not Found</h2>"

        self.wfile.write(html.encode('utf-8'))


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), RequestHandler)
    print("Сервер запущен на http://localhost:8080")
    server.serve_forever()