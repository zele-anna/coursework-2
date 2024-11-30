from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, sort_vacancies
from src.vacancies import Vacancy


def test_filter_vacancies(hh_data):
    vacancies_list = Vacancy.cast_to_object_list(hh_data)
    filtered_vacancies = filter_vacancies(vacancies_list, ["аналитик"])
    assert filtered_vacancies[0].vacancy_id == "99579827"
    assert filtered_vacancies[0].name == "Системный аналитик"


def test_get_vacancies_by_salary(hh_data_2):
    vacancies_list = Vacancy.cast_to_object_list(hh_data_2)
    filtered_vacancies = get_vacancies_by_salary(vacancies_list, "100000-140000")
    assert filtered_vacancies[0].vacancy_id == "99579827"
    assert filtered_vacancies[0].name == "Системный аналитик"
    filtered_vacancies_2 = get_vacancies_by_salary(vacancies_list, "400000-500000")
    assert filtered_vacancies_2[0].vacancy_id == "111862583"
    assert filtered_vacancies_2[0].name == "Frontend-разработчик"
    filtered_vacancies_3 = get_vacancies_by_salary(vacancies_list, "10-90")
    assert filtered_vacancies_3[0].vacancy_id == "112182612"
    assert filtered_vacancies_3[0].name == "Frontend-разработчик"


def test_sort_vacancies(hh_data):
    vacancies_list = Vacancy.cast_to_object_list(hh_data)
    sorted_vacancies = sort_vacancies(vacancies_list)
    assert sorted_vacancies[0].vacancy_id == "99579827"
    assert sorted_vacancies[0].name == "Системный аналитик"


def test_get_top_vacancies(hh_data, hh_data_2):
    vacancies_list = Vacancy.cast_to_object_list(hh_data)
    vacancies_list += Vacancy.cast_to_object_list(hh_data_2)
    top_vacancies = get_top_vacancies(vacancies_list, 4)
    assert len(vacancies_list) == 6
    assert len(top_vacancies) == 4
