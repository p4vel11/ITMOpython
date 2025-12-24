class UserCurrency:
    def __init__(self, id_: int, user_id: int, currency_id: str):
        self.id = id_
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("UserCurrency ID must be a positive integer")
        self._id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("User ID must be a positive integer")
        self._user_id = value

    @property
    def currency_id(self):
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Currency ID must be a non-empty string")
        self._currency_id = value.strip()