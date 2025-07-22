from .business import Business


class Store:
    def __init__(self, store_id: int, store_name: str, store_business: Business) -> None:
        self._store_id = store_id
        self._store_name = store_name
        self._store_business = store_business

    @property
    def id(self) -> int:
        return self._store_id

    @property
    def name(self) -> str:
        return self._store_name

    @property
    def business_id(self) -> int:
        return self._store_business.id

    @property
    def business_name(self) -> str:
        return self._store_business.name

    def __repr__(self) -> str:
        return f'Store(id={self.id}, name={self.name})'
