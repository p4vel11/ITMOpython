
import unittest
import io
import requests
from unittest.mock import patch, Mock
from main import get_currencies, logger


class TestGetCurrencies(unittest.TestCase):

    @patch("main.requests.get")
    def test_valid_response(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 93.25},
                "EUR": {"Value": 101.7}
            }
        }
        mock_get.return_value = mock_response
        result = get_currencies(["USD", "EUR"])
        self.assertEqual(result, {"USD": 93.25, "EUR": 101.7})

    @patch("main.requests.get", side_effect=requests.exceptions.ConnectionError("Network down"))
    def test_connection_error(self, mock_get):
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"])

    @patch("main.requests.get")
    def test_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        with self.assertRaises(ValueError):
            get_currencies(["USD"])

    @patch("main.requests.get")
    def test_missing_valute(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Date": "2025-12-10"}
        mock_get.return_value = mock_response
        with self.assertRaises(KeyError):
            get_currencies(["USD"])

    @patch("main.requests.get")
    def test_currency_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Valute": {"USD": {"Value": 93.25}}}
        mock_get.return_value = mock_response
        with self.assertRaises(KeyError):
            get_currencies(["GBP"])


class TestLoggerDecorator(unittest.TestCase):

    def test_success(self):
        stream = io.StringIO()
        @logger(handle=stream)
        def f(x):
            return x * 2
        result = f(5)
        self.assertEqual(result, 10)
        log = stream.getvalue()
        self.assertIn("INFO: Вызов функции f(5)", log)
        self.assertIn("INFO: Функция f завершилась успешно. Результат: 10", log)

    def test_error(self):
        stream = io.StringIO()
        @logger(handle=stream)
        def bad():
            raise ValueError("oops")
        with self.assertRaises(ValueError):
            bad()
        log = stream.getvalue()
        self.assertIn("ERROR:", log)
        self.assertIn("ValueError", log)


class TestStreamWrite(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()
        self.wrapped = logger(handle=self.stream)(
            lambda: get_currencies(['USD'], url="https://invalid.example.com")
        )

    @patch("main.requests.get", side_effect=requests.exceptions.ConnectionError("Network down"))
    def test_logging_error(self, mock_get):
        with self.assertRaises(ConnectionError):
            self.wrapped()
        logs = self.stream.getvalue()
        self.assertIn("ERROR:", logs)
        self.assertIn("ConnectionError", logs)


if __name__ =="__main__":
    unittest.main()