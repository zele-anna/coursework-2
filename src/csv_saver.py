import csv
import os
from typing import Any

from src.base_saver import BaseSaver
from src.vacancies import Vacancy


class CSVSaver(BaseSaver):
    """Класс для работы с данными о вакансиях, хранимых в файлах формата CSV."""

    __directory_name: str = "data/"
    __filename: str
    __path: str

    def __init__(self, filename: str = "vacancies.csv") -> None:
        """Инициализатор JSONSaver."""
        self.__directory_name = "data/"
        self.__filename = filename
        self.__path = os.path.join(self.__directory_name, self.__filename)

    def get_vacancies_from_file(self) -> Any:
        """Получение списка вакансий из файла CSV."""
        try:
            with open(self.__path, "r", encoding="UTF-8") as file:
                vacancy_list = list()
                reader = csv.DictReader(file)
                for row in reader:
                    vacancy_list.append(row)
                return vacancy_list
        except FileNotFoundError:
            print("Файл не найден.")

    def add_vacancy(self, vacancy: Any) -> None:
        """Добавление данных объекта класса Vacancy в файл CSV."""
        # Проверка на принадлежность переменной классу
        if isinstance(vacancy, Vacancy):
            data_to_save = list()
            vacancy_to_add = vacancy.object_to_dict()
            is_duplicate = False
            if os.path.exists(self.__path):
                # Попытка загрузки данных из файла
                data_to_save = self.get_vacancies_from_file()
                # Поиск дубликата добавляемой вакансии
                for item in data_to_save:
                    if item["vacancy_id"] == vacancy_to_add["vacancy_id"]:
                        print("Вакансия уже есть в файле.")
                        is_duplicate = True
                        break
                # Запись обновленных данных в файл, если вакансия уникальна
                if is_duplicate is False:
                    data_to_save.append(vacancy_to_add)
                    with open(self.__path, "w", encoding="UTF-8") as file:
                        fieldnames = [
                            "vacancy_id",
                            "name",
                            "link",
                            "salary_from",
                            "salary_to",
                            "salary_range",
                            "employer",
                            "requirement",
                            "employment",
                            "schedule",
                        ]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        for item in data_to_save:
                            writer.writerow(item)
                        print("Вакансия успешно добавлена.")
            else:
                # Создание файла, если файл не найден
                with open(self.__path, "w", encoding="UTF-8", newline="") as file:
                    data_to_save.append(vacancy_to_add)
                    fieldnames = [
                        "vacancy_id",
                        "name",
                        "link",
                        "salary_from",
                        "salary_to",
                        "salary_range",
                        "employer",
                        "requirement",
                        "employment",
                        "schedule",
                    ]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for item in data_to_save:
                        writer.writerow(item)
                    print("Создан файл и успешно добавлена вакансия.")

        else:
            print("Переданный объект не является объектом класса Vacancy.")

    def delete_vacancy(self, vacancy: Any) -> None:
        """Удаление вакансии из файла JSON."""
        # Проверка принадлежности переменной классу
        if isinstance(vacancy, Vacancy):
            data_to_save = list()
            vacancy_to_delete = vacancy.object_to_dict()
            is_found = False
            if os.path.exists(self.__path):
                # Получение данных из файла
                data_to_save = self.get_vacancies_from_file()
                # Проверка списка на наличие переданной вакансии и удаление вакансии, если найдена
                for item in data_to_save:
                    if item["vacancy_id"] == vacancy_to_delete["vacancy_id"]:
                        data_to_save.remove(item)
                        is_found = True
                # Запись обновленных данных в файл
                if is_found:
                    with open(self.__path, "w", encoding="UTF-8", newline="") as file:
                        fieldnames = [
                            "vacancy_id",
                            "name",
                            "link",
                            "salary_from",
                            "salary_to",
                            "salary_range",
                            "employer",
                            "requirement",
                            "employment",
                            "schedule",
                        ]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        for item in data_to_save:
                            writer.writerow(item)
                        print("Вакансия успешно удалена.")
                else:
                    print("Вакансия не найдена в файле.")
            else:
                print("Файл не найден.")
        else:
            print("Переданный объект не является объектом класса Vacancy.")
