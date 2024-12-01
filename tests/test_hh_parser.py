# from unittest.mock import patch
#
# from typing import Any
#
# from src.hh_parser import HeadHunterAPI
#
#
# @patch("src.hh_parser.requests.get")
# def test_get_vacancies(mock_get: Any, hh_response: dict, hh_data: list) -> None:
#     """Тест на проверку работы метода получения данных hh.ru."""
#     hh_parser = HeadHunterAPI()
#     hh_parser.get_vacancies("разработчик")
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = hh_response
#     assert hh_parser.vacancies == hh_data
