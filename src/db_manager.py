import json

import psycopg2

from config import config


class DBManager:
    """Класс для работы с базой данный по вакансиям."""

    def __init__(self, db_name: str) -> None:
        """Инициализация экземпляра класса базы данных и создание новой базы данных."""
        self.__db_name = db_name
        self.__params = config()
        # self.__conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

    def create_database(self) -> None:

        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"DROP DATABASE {self.__db_name}")
            print("База удалена.")
        except Exception:
            print("База не найдена.")
        finally:
            cur.execute(f"CREATE DATABASE {self.__db_name}")
            print("Создана новая база.")

        cur.close()
        conn.close()

    # def drop_database(self) -> None:
    #     """Удаление базы данных."""
    #     conn = psycopg2.connect(dbname="postgres", **self.__params)
    #     conn.autocommit = True
    #     cur = conn.cursor()
    #
    #     cur.execute(f"DROP DATABASE {self.__db_name}")
    #
    #     cur.commit()
    #     cur.close()
    #     conn.close()

    def create_tables(self) -> None:
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    employer_name VARCHAR (255) NOT NULL,
                    employer_url TEXT
                )
            """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancy_name VARCHAR (255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR (3),
                    type TEXT,
                    employer_id INT REFERENCES employers(employer_id),
                    requirement TEXT,
                    employment VARCHAR (50),
                    schedule VARCHAR (50),
                    vacancy_url TEXT
                )
            """
            )

        conn.commit()
        conn.close()

    def save_data_to_db(self, data: list) -> None:
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        employer_data = list()
        for item in data:
            employer_elem = dict()
            employer_elem["id"] = item["employer"]["id"]
            employer_elem["name"] = item["employer"]["name"]
            employer_elem["alternate_url"] = item["employer"]["alternate_url"]
            if employer_elem in employer_data:
                continue
            else:
                employer_data.append(employer_elem)

        with conn.cursor() as cur:
            for employer in employer_data:
                cur.execute(
                    """
                    INSERT INTO employers (employer_id, employer_name, employer_url)
                    VALUES (%s, %s, %s)
                    """,
                    (employer["id"], employer["name"], employer["alternate_url"]),
                )
            for item in data:
                salary_from = None
                salary_to = None
                salary_currency = None
                salary_data = item["salary"]
                if salary_data:
                    salary_from = salary_data["from"]
                    salary_to = salary_data["to"]
                    salary_currency = salary_data["currency"]

                cur.execute(
                    """
                    INSERT INTO vacancies (
                    vacancy_name,
                    salary_from,
                    salary_to,
                    salary_currency,
                    type,
                    employer_id,
                    requirement,
                    employment,
                    schedule,
                    vacancy_url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        item["name"],
                        salary_from,
                        salary_to,
                        salary_currency,
                        item["type"]["name"],
                        item["employer"]["id"],
                        item["snippet"]["requirement"],
                        item["employment"]["name"],
                        item["schedule"]["name"],
                        item["alternate_url"],
                    ),
                )

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self) -> str:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT emp.employer_name, COUNT(vacancy_id) FROM vacancies
                JOIN employers as emp USING(employer_id)
                GROUP BY employer_name
                """
            )
            data = cur.fetchall()

        conn.close()

        result = dict()

        for item in data:
            result[item[0]] = item[1]

        return json.dumps(result, ensure_ascii=False)

    def get_all_vacancies(self) -> str:
        """Получает список всех вакансий с указанием названия компании, названия вакансии,
        зарплаты (от, до, валюта) и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                emp.employer_name,
                vacancy_name,
                salary_from,
                salary_to,
                salary_currency,
                vacancy_url
                FROM vacancies
                JOIN employers as emp USING(employer_id)
                """
            )
            data = cur.fetchall()

        conn.close()

        result_list = list()

        for item in data:
            vacancy_elem = dict()
            vacancy_elem["employer_name"] = item[0]
            vacancy_elem["vacancy_name"] = item[1]
            vacancy_elem["salary_from"] = item[2]
            vacancy_elem["salary_to"] = item[3]
            vacancy_elem["salary_currency"] = item[4]
            vacancy_elem["vacancy_url"] = item[5]
            result_list.append(vacancy_elem)

        result = dict()
        result["items"] = result_list

        return json.dumps(result, ensure_ascii=False)

    def get_avg_salary(self) -> str:
        """Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_from + salary_to)/2) FROM vacancies
                """
            )
            data = cur.fetchall()

        conn.close()

        result = dict()
        result["avg_salary"] = round(float(data[0][0]), 2)

        return json.dumps(result, ensure_ascii=False)

    def get_vacancies_with_higher_salary(self) -> str:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                emp.employer_name,
                vacancy_name,
                salary_from,
                salary_to,
                salary_currency,
                vacancy_url
                FROM vacancies
                JOIN employers as emp USING(employer_id)
                WHERE (salary_from + salary_to)/2 > {json.loads(avg_salary)["avg_salary"]}
                """
            )
            data = cur.fetchall()

        conn.close()

        result_list = list()

        for item in data:
            vacancy_elem = dict()
            vacancy_elem["employer_name"] = item[0]
            vacancy_elem["vacancy_name"] = item[1]
            vacancy_elem["salary_from"] = item[2]
            vacancy_elem["salary_to"] = item[3]
            vacancy_elem["salary_currency"] = item[4]
            vacancy_elem["vacancy_url"] = item[5]
            result_list.append(vacancy_elem)

        result = dict()
        result["items"] = result_list

        return json.dumps(result, ensure_ascii=False)

    def get_vacancies_with_keyword(self, keyword: str) -> str:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                f"""
                        SELECT
                        emp.employer_name,
                        vacancy_name,
                        salary_from,
                        salary_to,
                        salary_currency,
                        vacancy_url
                        FROM vacancies
                        JOIN employers as emp USING(employer_id)
                        WHERE vacancy_name LIKE '%{keyword}%'
                        """
            )
            data = cur.fetchall()

        conn.close()

        result_list = list()

        for item in data:
            vacancy_elem = dict()
            vacancy_elem["employer_name"] = item[0]
            vacancy_elem["vacancy_name"] = item[1]
            vacancy_elem["salary_from"] = item[2]
            vacancy_elem["salary_to"] = item[3]
            vacancy_elem["salary_currency"] = item[4]
            vacancy_elem["vacancy_url"] = item[5]
            result_list.append(vacancy_elem)

        result = dict()
        result["items"] = result_list

        return json.dumps(result, ensure_ascii=False)
