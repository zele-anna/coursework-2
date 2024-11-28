from typing import Any
import requests

from abc import ABC, abstractmethod

class Parser(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_vacancies(self, keyword):
        """Абстрактный метод для загрузки данных из API."""
        pass


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter."""

    def __init__(self) -> None:
        """Инициализация объекта обращения к API HeadHunter."""
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []
        # super().__init__(file_worker)

    def get_vacancies(self, keyword: str) -> list:
        """Метод загрузки данных из API по ключевому слову."""
        self.__params['text'] = keyword
        while self.__params.get('page') != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()['items']
            self.__vacancies.extend(vacancies)
            self.__params['page'] += 1
        return self.__vacancies

    @property
    def vacancies(self):
        return self.__vacancies


if __name__ == "__main__":
    hh_parser = HeadHunterAPI()
    hh_parser.get_vacancies("тестировщик квартир")
    print(hh_parser.vacancies)
    print(len(hh_parser.vacancies))
