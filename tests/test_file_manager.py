from unittest.mock import patch

from src.file_manager import JSONSaver


@patch("src.file_manager.json.load")
def test_json_saver(mocked_load, file_data, vacancy_object, capsys):
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
