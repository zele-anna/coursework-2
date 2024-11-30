from src.vacancies import Vacancy


def test_vacancy_init():
    vacancy = Vacancy(
        "123",
        "Python Developer",
        "<https://hh.ru/vacancy/123456>",
        "100000-150000 руб.",
        "Яндекс",
        "Требования: опыт работы от 3 лет...",
        "Частичная занятость",
        "Удаленная работа",
    )
    assert vacancy.vacancy_id == "123"
    assert vacancy.name == "Python Developer"
    assert vacancy.link == "<https://hh.ru/vacancy/123456>"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.salary_range == "100000-150000 руб."
    assert vacancy.employer == "Яндекс"
    assert vacancy.requirement == "Требования: опыт работы от 3 лет..."
    assert vacancy.employment == "Частичная занятость"
    assert vacancy.schedule == "Удаленная работа"


def test_cast_to_object_list(hh_data):
    vacancies_list = Vacancy.cast_to_object_list(hh_data)
    assert len(vacancies_list) == 3
    assert vacancies_list[0].vacancy_id == "111862583"
    assert vacancies_list[0].name == "Frontend-разработчик"
    assert vacancies_list[0].link == "https://hh.ru/vacancy/111862583"
    assert vacancies_list[0].salary_from == 0
    assert vacancies_list[0].salary_to == 0
    assert vacancies_list[0].salary_range == "Зарплата не указана"
    assert vacancies_list[0].employer == "VODIY SOFT HUB"
    assert (
        vacancies_list[0].requirement
        == "React TypeScript yoki Next.js TypeScript bo‘yicha bilim."
    )
    assert vacancies_list[0].employment == "Полная занятость"
    assert vacancies_list[0].schedule == "Полный день"
    assert vacancies_list[1].salary_from == 2000000
    assert vacancies_list[1].salary_to == 10000000
    assert vacancies_list[1].salary_range == "2000000-10000000 UZS"
    print(vacancies_list)


def test_object_to_dict(vacancy_object, vacancy_dict):
    vacancy_obj_to_dict = vacancy_object.object_to_dict()
    assert vacancy_obj_to_dict == vacancy_dict


def test_get_salary_data_from_dict():
    salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_dict(
        {"from": 2000000, "to": 10000000, "currency": "UZS", "gross": False}
    )
    assert salary_from == 2000000
    assert salary_to == 10000000
    assert salary_range == "2000000-10000000 UZS"
    salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_dict(
        {"from": 2000000, "to": None, "currency": "UZS", "gross": False}
    )
    assert salary_from == 2000000
    assert salary_to == 0
    assert salary_range == "От 2000000 UZS"
    salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_dict(
        {"from": None, "to": 10000000, "currency": "UZS", "gross": False}
    )
    assert salary_from == 0
    assert salary_to == 10000000
    assert salary_range == "До 10000000 UZS"


def test_get_salary_data_from_str():
    salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_str("2000000-10000000 UZS")
    assert salary_from == 2000000
    assert salary_to == 10000000
    assert salary_range == "2000000-10000000 UZS"
    salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_str("От 2000000 UZS")
    assert salary_from == 2000000
    assert salary_to == 0
    assert salary_range == "От 2000000 UZS"
    salary_from, salary_to, salary_range = Vacancy.get_salary_data_from_str("До 10000000 UZS")
    assert salary_from == 0
    assert salary_to == 10000000
    assert salary_range == "До 10000000 UZS"
