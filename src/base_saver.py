from abc import ABC, abstractmethod
from typing import Any


class BaseSaver(ABC):
    """Абстрактный класс для работы с данными о вакансиях."""

    __directory_name: str
    __filename: str
    __path: str

    @abstractmethod
    def get_vacancies_from_file(self) -> None:
        """Абстрактный метод получения данных о вакансиях из файла."""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Any) -> None:
        """Абстрактный метод добавления объекта класса Vacancy в файл."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Any) -> None:
        """Абстрактный метод удаления объекта класса Vacancy из файла."""
        pass
