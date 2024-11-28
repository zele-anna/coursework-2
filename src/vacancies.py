import json

class Vacancy:
    """Класс для создания объектов-вакансий."""
    vacancy_id: int
    name: str
    link: str
    salary: str
    employer: str
    requirement: str
    employment: str
    schedule: str

    def __init__(self, vacancy_id, name, link, salary, employer, requirement, employment, schedule):
        """Метод инициализации объектов класса Vacancy."""
        self.vacancy_id = vacancy_id
        self.name = name
        self.link = link
        self.salary = salary
        self.employer = employer
        self.requirement = requirement
        self.employment = employment
        self.schedule = schedule

    @classmethod
    def cast_to_object_list(cls, data: list) -> list:
        """Класс-метод для создания списка объектов вакансий из списка словарей с данными."""

        obj_list = list()

        for item in data:

            # Определение формата вывода данных о зарплате
            salary = ""
            if item["salary"] is None:
                salary = "Зарплата не указана"
            elif item["salary"]["from"] and item["salary"]["to"]:
                salary = f'{item["salary"]["from"]}-{item["salary"]["to"]} {item["salary"]["currency"]} {"на руки" if item["salary"]["gross"] == False else "до налога"}'
            elif item["salary"]["from"]:
                salary = f'От {item["salary"]["from"]} {item["salary"]["currency"]} {"на руки" if item["salary"]["gross"] == False else "до налога"}'
            elif item["salary"]["to"]:
                salary = f'До {item["salary"]["to"]} {item["salary"]["currency"]} {"на руки" if item["salary"]["gross"] == False else "до налога"}'

            # Инициализация объектов класса и добавление их в список объектов
            new_vacancy = cls(
                item["id"],
                item["name"],
                item["alternate_url"],
                salary,
                item["employer"]["name"],
                item["snippet"]["requirement"],
                item["employment"]["name"],
                item["schedule"]["name"],
            )
            obj_list.append(new_vacancy)
        return obj_list
