class User:
    def __init__(self, id_: int, name: str):
        self.id = id_
        self.name = name


    @property
    def id(self):
        return self._id


    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("User ID must be a positive integer")
        self._id = value


    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("User name must be a non-empty string")
        self._name = value.strip()