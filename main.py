from src.parsers import HeadHunterAPI
from src.vacancies import Vacancy

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("тестировщик квартир")

# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

# Пример работы контструктора класса с одной вакансией
vacancy = Vacancy(123, "Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Яндекс", "Требования: опыт работы от 3 лет...", "Частичная занятость", "Удаленная работа")

# Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HeadHunter"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)


if __name__ == "__main__":
    # user_interaction()
    for item1 in hh_vacancies[16:19]:
        print(item1["salary"])
    for item in vacancies_list[16:19]:
        print("\nВакансия")
        print(item.vacancy_id)
        print(item.name)
        print(item.link)
        print(item.salary)
        print(item.employer)
        print(item.requirement)
        print(item.employment)
        print(item.schedule)

    # print(vacancy.vacancy_id)
    # print(vacancy.name)
    # print(vacancy.link)
    # print(vacancy.salary)
    # print(vacancy.employer)
    # print(vacancy.requirement)
    # print(vacancy.employment)
    # print(vacancy.schedule)
