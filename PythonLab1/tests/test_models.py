import unittest
from models import User, Currency

class TestModels(unittest.TestCase):
    def test_user_valid(self):
        u = User(1, "Alice")
        self.assertEqual(u.name, "Alice")

    def test_user_invalid_id(self):
        with self.assertRaises(ValueError):
            User(-1, "Bob")

    def test_currency_valid(self):
        c = Currency("R01235", "840", "USD", "Доллар США", 75.5, 1)
        self.assertEqual(c.char_code, "USD")

    def test_currency_invalid_nominal(self):
        with self.assertRaises(ValueError):
            Currency("R01235", "840", "USD", "Доллар", 75.5, -1)

if __name__ == "__main__":
    unittest.main()