# from unittest.mock import patch
#
# from src.parsers import HeadHunterAPI
#
#
# @patch("src.parsers.requests.get")
# def test_get_vacancies(mock_get, hh_response, hh_data):
#     hh_parser = HeadHunterAPI()
#     hh_parser.get_vacancies("разработчик")
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = hh_response
#     assert hh_parser.vacancies == hh_data
