import re


class Vacancy:
    """Класс для создания объектов-вакансий."""

    vacancy_id: str
    name: str
    link: str
    salary_from: float | None
    salary_to: float | None
    salary_range: str
    employer: str
    requirement: str
    employment: str
    schedule: str

    def __init__(
        self,
        vacancy_id: str,
        name: str,
        link: str,
        salary: str | dict,
        employer: str,
        requirement: str,
        employment: str,
        schedule: str,
    ) -> None:
        """Метод инициализации объектов класса Vacancy."""
        salary_from = 0
        salary_to = 0
        salary_range = ""
        if salary is None:
            salary_range = "Зарплата не указана"
        elif type(salary) is dict:
            salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_dict(salary)
        elif type(salary) is str:
            salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_str(salary)
        self.vacancy_id: str = vacancy_id
        self.name: str = name
        self.link: str = link
        self.salary_from: int = int(salary_from)
        self.salary_to: int = int(salary_to)
        self.salary_range: str = salary_range
        self.employer: str = employer
        self.requirement: str = requirement
        self.employment: str = employment
        self.schedule: str = schedule

    @classmethod
    def cast_to_object_list(cls, data: list) -> list:
        """Класс-метод для создания списка объектов вакансий из списка словарей с данными."""

        obj_list = list()

        for item in data:
            # Инициализация объектов класса и добавление их в список объектов
            new_vacancy = cls(
                item["id"],
                item["name"],
                item["alternate_url"],
                item["salary"],
                item["employer"]["name"],
                item["snippet"]["requirement"],
                item["employment"]["name"],
                item["schedule"]["name"],
            )
            obj_list.append(new_vacancy)
        return obj_list

    def object_to_dict(self) -> dict:
        """Метод для преобразования объекта класса в словарь значений."""
        vacancy_dict: dict = dict()
        vacancy_dict["vacancy_id"] = self.vacancy_id
        vacancy_dict["name"] = self.name
        vacancy_dict["link"] = self.link
        vacancy_dict["salary_from"] = self.salary_from
        vacancy_dict["salary_to"] = self.salary_to
        vacancy_dict["salary_range"] = self.salary_range
        vacancy_dict["employer"] = self.employer
        vacancy_dict["requirement"] = self.requirement
        vacancy_dict["employment"] = self.employment
        vacancy_dict["schedule"] = self.schedule
        return vacancy_dict

    @staticmethod
    def get_salary_data_from_dict(salary_data: dict) -> tuple:
        """Определение значений по зарплате из словаря: от, до и диапазон."""
        salary_from = 0
        salary_to = 0
        salary_range = ""
        if salary_data["from"] and salary_data["to"]:
            salary_from = salary_data["from"]
            salary_to = salary_data["to"]
            salary_range = f'{salary_data["from"]}-{salary_data["to"]} {salary_data["currency"]}'
        elif salary_data["from"]:
            salary_from = salary_data["from"]
            salary_range = f'От {salary_data["from"]} {salary_data["currency"]}'
        elif salary_data["to"]:
            salary_to = salary_data["to"]
            salary_range = f'До {salary_data["to"]} {salary_data["currency"]}'
        return salary_from, salary_to, salary_range

    @staticmethod
    def get_salary_data_from_str(salary_data: str) -> tuple:
        """Определение значений по зарплате из строки: от, до и диапазон."""
        salary_from = 0
        salary_to = 0
        salary_range = salary_data
        salary_data = salary_data.replace(" ", "")
        if "-" in salary_data:
            salary_from, salary_to = re.findall(r"\d+", salary_data, flags=0)
        elif "До".lower() in salary_data.lower():
            salary_to = re.findall(r"\d+", salary_data, flags=0)[0]
        elif "От".lower() in salary_data.lower():
            salary_from = re.findall(r"\d+", salary_data, flags=0)[0]
        return int(salary_from), int(salary_to), salary_range
