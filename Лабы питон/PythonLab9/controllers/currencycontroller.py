from models.currency import Currency
from controllers.databasecontroller import CurrencyRatesCRUD
from typing import List, Dict, Any

class CurrencyController:
    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def create_currency(self, data: Dict[str, Any]) -> int:
        return self.db.create(data)

    def list_currencies(self) -> List[Dict]:
        rows = self.db.read_all()
        return [dict(row) for row in rows]

    def update_currency(self, char_code: str, value: float):
        self.db.update(char_code, value)

    def delete_currency(self, currency_id: int):
        self.db.delete(currency_id)

    def get_currency_by_char_code(self, char_code: str):
        row = self.db.read_by_char_code(char_code)
        return dict(row) if row else None