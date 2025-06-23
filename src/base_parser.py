from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def _connect(self, keyword: str) -> None:
        """Абстрактный метод подключения к API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> None:
        """Абстрактный метод для загрузки данных из API."""
        pass
