import typing

from pyoro.exceptions.already_initialized import AlreadyInitializedException

T = typing.TypeVar("T")


class Bank(typing.Generic[T]):
    _instance = None

    @classmethod
    def build(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.load()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise AlreadyInitializedException(
                f"Bank '{self.__class__.__name__}' already initialized"
            )
        self.data: dict[str, T] = {}

    def load(self):
        pass

    def get(self, key: str) -> T:
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found in bank '{self.__class__.__name__}'")
        return self.data[key]

    def __getitem__(self, key: str):
        return self.get(key)
