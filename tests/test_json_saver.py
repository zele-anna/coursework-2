from typing import Any
from unittest.mock import patch

from src.json_saver import JSONSaver


@patch("src.json_saver.json.load")
def test_json_saver(mocked_load: Any, file_data: dict, vacancy_object: Any, capsys: Any) -> None:
    mocked_load.return_value = file_data
    json_saver = JSONSaver()
    assert json_saver.get_vacancies_from_file() == file_data
    json_saver.add_vacancy(vacancy_object)
    message = capsys.readouterr()
    assert message.out.strip() == "Вакансия успешно добавлена."
    json_saver.add_vacancy(vacancy_object)
    message = capsys.readouterr()
    assert message.out.strip() == "Вакансия уже есть в файле."
    json_saver.delete_vacancy(vacancy_object)
    message = capsys.readouterr()
    assert message.out.strip() == "Вакансия успешно удалена."
    json_saver.delete_vacancy(vacancy_object)
    message = capsys.readouterr()
    assert message.out.strip() == "Вакансия не найдена в файле."


def test_json_saver_get_vacancies_no_file(capsys: Any, vacancy_object: Any) -> None:
    json_saver = JSONSaver("test")
    json_saver.get_vacancies_from_file()
    message = capsys.readouterr()
    assert message.out == "Файл не найден.\n"
    json_saver.delete_vacancy(vacancy_object)
    message = capsys.readouterr()
    assert message.out == "Файл не найден.\n"
