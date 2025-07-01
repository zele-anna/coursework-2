from src.csv_saver import CSVSaver
from src.db_manager import DBManager
from src.hh_parser import HeadHunterAPI
from src.json_saver import JSONSaver
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancies import Vacancy

# Пример работы конструктора класса с одной вакансией
vacancy = Vacancy(
    "123",
    "Python Developer",
    "<https://hh.ru/vacancy/123456>",
    "10000-1500000 руб.",
    "1",
    "Яндекс",
    "Требования: опыт работы от 3 лет...",
    "Частичная занятость",
    "Удаленная работа",
)
vacancy_3 = Vacancy(
    "121",
    "Python Developer",
    "<https://hh.ru/vacancy/123456>",
    "100 000-150 000 руб.",
    "1",
    "Яндекс",
    "Требования: опыт работы от 3 лет...",
    "Частичная занятость",
    "Удаленная работа",
)

# print(vacancy.vacancy_id)
# print(vacancy.name)
# print(vacancy.link)
# print(vacancy.salary_from)
# print(vacancy.salary_to)
# print(vacancy.salary_range)
# print(vacancy.employer)
# print(vacancy.requirement)
# print(vacancy.employment)
# print(vacancy.schedule)

# Преобразование объекта класса Vacancy в словарь
# vacancy_dict = vacancy.object_to_dict()

# Пример работы с файлами JSON
json_saver = JSONSaver()
# json_saver_2 = JSONSaver("user_vacancies.json")

# Сохранение информации о вакансиях в файл JSON
# json_saver.add_vacancy(vacancy)
# json_saver_2.add_vacancy(vacancy_3)
# json_saver.get_vacancies_from_file()
# json_saver_2.get_vacancies_from_file()
# json_saver.delete_vacancy(vacancy)
# json_saver_2.delete_vacancy(vacancy_3)

# Пример работы с файлами CSV
csv_saver = CSVSaver()
# csv_saver_2 = CSVSaver("user_vacancies.csv")

# Сохранение информации о вакансиях в файл CSV
# csv_saver.add_vacancy(vacancy)
# csv_saver_2.add_vacancy(vacancy_3)
# csv_saver.get_vacancies_from_file()
# csv_saver_2.get_vacancies_from_file()
# csv_saver.delete_vacancy(vacancy)
# csv_saver_2.delete_vacancy(vacancy_3)

# Сравнение вакансий по зарплате
# print(vacancy == vacancy_3)
# print(vacancy > vacancy_3)
# print(vacancy >= vacancy_3)
# print(vacancy < vacancy_3)
# print(vacancy <= vacancy_3)


# Функция для взаимодействия с пользователем
def user_interaction() -> None:
    # platforms = ["HeadHunter"]
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()

    search_query = input("Введите поисковый запрос: ")

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies(search_query)

    # Преобразование набора данных из JSON в список объектов
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    # Фильтрация полученного списка вакансий по ключевым словам
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    # Фильтрация списка вакансий по диапазону зарплат
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000-150000
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    # Сортировка списка вакансий по зарплате
    sorted_vacancies = sort_vacancies(ranged_vacancies)

    # Вывод топ-N по зарплате
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод данных полученного списка вакансий
    print_vacancies(top_vacancies)


def main() -> None:
    # Создание списка работодателей (по ID на сайте HeadHunter)
    employers = [
        "2324020",  # Точка
        "1455",  # HH
        "999442",  # amoCRM
        "1740",  # Яндекс
        "78638",  # ТБанк
        "2180",  # Ozon Офис и Коммерция
        "11631298",  # Эквариум
        "819979",  # SkillStaff
        "9712671",  # Зебра
        "2136954",  # Домклик
    ]

    # Создание класса для работы с базой данных "db_vacancies" (БД)
    db_vacancies = DBManager("db_vacancies")

    # Создание БД
    db_vacancies.create_database()
    # Создание таблиц БД
    db_vacancies.create_tables()

    # Создание класса для работы с API HeadHunter
    hh_api = HeadHunterAPI()
    # Получение данных о вакансиях по списку работодателей
    data = hh_api.get_vacancies_by_employer(employers)
    # Сохранение полученных данных в таблицы employers и vacancies БД
    db_vacancies.save_data_to_db(data)

    # Получение данных из БД по компаниям и количеству вакансий каждой из них (JSON)
    db_vacancies.get_companies_and_vacancies_count()
    # Получение данных из БД по всем вакансиям (JSON)
    db_vacancies.get_all_vacancies()
    # Получение данных из БД по средней зарплате (JSON)
    db_vacancies.get_avg_salary()
    # Получение данных из БД по вакансиям с зарплатой выше средней (JSON)
    db_vacancies.get_vacancies_with_higher_salary()
    # Получение данных из БД по всем вакансиям, содержащих ключевое слово в наименовании (JSON)
    db_vacancies.get_vacancies_with_keyword("Python")


if __name__ == "__main__":
    # user_interaction()
    main()
