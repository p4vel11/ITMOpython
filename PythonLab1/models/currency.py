class Currency:
    def __init__(self, id_: str, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.id = id_
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal


    @property
    def id(self):
        return self._id


    @id.setter
    def id(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Currency ID must be a non-empty string")
        self._id = value.strip()


    @property
    def num_code(self):
        return self._num_code


    @num_code.setter
    def num_code(self, value):
        if not isinstance(value, str) or len(value) != 3:
            raise ValueError("NumCode must be a 3-digit string")
        self._num_code = value


    @property
    def char_code(self):
        return self._char_code


    @char_code.setter
    def char_code(self, value):
        if not isinstance(value, str) or len(value) != 3:
            raise ValueError("CharCode must be a 3-letter code")
        self._char_code = value


    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Currency name must be a non-empty string")
        self._name = value.strip()


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Currency value must be a positive number")
        self._value = float(value)


    @property
    def nominal(self):
        return self._nominal


    @nominal.setter
    def nominal(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Nominal must be a positive integer")
        self._nominal = value