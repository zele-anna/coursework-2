from src.file_manager import JSONSaver
from src.parsers import HeadHunterAPI
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancies import Vacancy

# Пример работы конструктора класса с одной вакансией
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

print(vacancy.vacancy_id)
print(vacancy.name)
print(vacancy.link)
print(vacancy.salary_from)
print(vacancy.salary_to)
print(vacancy.salary_range)
print(vacancy.employer)
print(vacancy.requirement)
print(vacancy.employment)
print(vacancy.schedule)

# Преобразование объекта класса Vacancy в словарь
vacancy_dict = vacancy.object_to_dict()
print(vacancy_dict)

# Пример работы с файлами
json_saver = JSONSaver()
vacancy_3 = Vacancy(
    "121",
    "Python Developer",
    "<https://hh.ru/vacancy/123456>",
    "100 000-150 000 руб.",
    "Яндекс",
    "Требования: опыт работы от 3 лет...",
    "Частичная занятость",
    "Удаленная работа",
)
json_saver.add_vacancy(vacancy_3)
print(len(json_saver.get_vacancies_from_file()))
json_saver.delete_vacancy(vacancy_3)
print(len(json_saver.get_vacancies_from_file()))


# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.delete_vacancy(vacancy)


# Функция для взаимодействия с пользователем
def user_interaction() -> None:
    # platforms = ["HeadHunter"]
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()

    search_query = input("Введите поисковый запрос: ")

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies(search_query)
    print(hh_vacancies[:10]["salary"])

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


if __name__ == "__main__":
    user_interaction()
