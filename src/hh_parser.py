from typing import Any

import requests

from src.base_parser import Parser


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter."""

    def __init__(self) -> None:
        """Инициализация объекта обращения к API HeadHunter."""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: Any = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies: list = []
        # super().__init__(file_worker)

    def get_vacancies(self, keyword: str) -> Any:
        """Метод загрузки данных из API по ключевому слову."""
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
            else:
                print(f"Ошибка работы с API, код {response.status_code}")
        return self.__vacancies

    @property
    def vacancies(self) -> Any:
        """Геттер показателя __vacancies"""
        return self.__vacancies


if __name__ == "__main__":
    hh_parser = HeadHunterAPI()
    hh_parser.get_vacancies("тестировщик квартир")
    print(hh_parser.vacancies)
    print(len(hh_parser.vacancies))
