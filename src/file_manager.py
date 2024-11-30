import json
from abc import ABC, abstractmethod
from typing import Any

from src.vacancies import Vacancy


class FileManager(ABC):
    """Абстрактный класс для работы с данными о вакансиях."""

    path: str

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


class JSONSaver(FileManager):
    """Класс для работы с данными о вакансиях, хранимых в файлах формата JSON."""

    def __init__(self) -> None:
        """Инициализатор JSONSaver."""
        self.path = "data/vacancies.json"

    def get_vacancies_from_file(self) -> Any:
        """Получение списка вакансий из файла JSON."""
        try:
            with open(self.path, "r", encoding="UTF-8") as file:
                vacancy_list = json.load(file)
        except FileNotFoundError:
            print("Файл не найден.")
        return vacancy_list

    def add_vacancy(self, vacancy: Any) -> None:
        """Добавление данных объекта класса Vacancy в файл JSON."""
        # Проверка на принадлежность переменной классу
        if isinstance(vacancy, Vacancy):
            data_to_save: dict = dict()
            data_to_save["items"] = list()
            vacancy_to_add = vacancy.object_to_dict()
            duplicate = False
            try:
                # Загрузка данных из файла
                data_to_save = self.get_vacancies_from_file()
            except FileNotFoundError:
                # Создание файла, если файл не найден
                with open(self.path, "w", encoding="UTF-8") as file:
                    data_to_save["items"].append(vacancy_to_add)
                    json.dump(data_to_save, file, indent=4, ensure_ascii=False)
                    print("Создан файл и успешно добавлена вакансия.")
            else:
                # Поиск дубликата добавляемой вакансии
                for item in data_to_save["items"]:
                    if item["vacancy_id"] == vacancy_to_add["vacancy_id"]:
                        print("Вакансия уже есть в файле.")
                        duplicate = True
                        break
                # Запись обновленных данных в файл, если вакансия уникальна
                if duplicate is False:
                    data_to_save["items"].append(vacancy_to_add)
                    with open(self.path, "w", encoding="UTF-8") as file:
                        json.dump(data_to_save, file, indent=4, ensure_ascii=False)
                        print("Вакансия успешно добавлена.")
        else:
            print("Переданный объект не является объектом класса Vacancy.")

    def delete_vacancy(self, vacancy: Any) -> None:
        """Удаление вакансии из файла JSON."""
        # Проверка принадлежности переменной классу
        if isinstance(vacancy, Vacancy):
            data_to_save: dict = dict()
            data_to_save["items"] = list()
            vacancy_to_delete = vacancy.object_to_dict()
            is_found = False
            try:
                # Получение данных из файла
                data_to_save = self.get_vacancies_from_file()
            except FileNotFoundError:
                print("Файл не найден.")
            else:
                # Проверка списка на наличие переданной вакансии и удаление вакансии, если найдена
                for item in data_to_save["items"]:
                    if item["vacancy_id"] == vacancy_to_delete["vacancy_id"]:
                        data_to_save["items"].remove(item)
                        is_found = True
                # Запись обновленных данных в файл
                if is_found:
                    with open(self.path, "w", encoding="UTF-8") as file:
                        json.dump(data_to_save, file, indent=4, ensure_ascii=False)
                        print("Вакансия успешно удалена.")
                else:
                    print("Вакансия не найдена в файле.")
        else:
            print("Переданный объект не является объектом класса Vacancy.")
