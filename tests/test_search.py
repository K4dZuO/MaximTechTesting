import pytest
import logging
from pydantic import ValidationError


from models.search import SearchQuery, SearchResponse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def test_search_response_valid():
    response_data = {
        "total": 5,
        "objectIDs": [1, 2, 3, 4, 5]
    }
    logger.info(f"Тест: Проверка корректного ответа на запрос. Данные: {response_data}")
    response = SearchResponse(**response_data)
    
    logger.info(f"Проверка: total = {response.total}, objectIDs = {response.objectIDs}")
    assert response.total == 5
    assert response.objectIDs == [1, 2, 3, 4, 5]


def test_search_response_missing_field():
    response_data = {
        "total": 5
    }
    logger.info(f"Тест: Проверка ответа с отсутствующим полем. Данные: {response_data}")
    with pytest.raises(ValidationError):
        SearchResponse(**response_data)
        logger.error(f"Ошибка: отсутствует обязательное поле 'objectIDs' в ответе.")


def test_search_query_valid():
    query_data = {
        "q": "sunflowers",
        "isHighlight": True,
        "medium": "Paintings"
    }
    logger.info(f"Тест: Проверка корректного запроса. Данные: {query_data}")
    query = SearchQuery(**query_data)
    
    logger.info(f"Проверка: q = {query.q}, isHighlight = {query.isHighlight}, medium = {query.medium}")
    assert query.q == "sunflowers"
    assert query.isHighlight is True
    assert query.medium == "Paintings"


def test_search_query_invalid_type():
    query_data = {
        "q": "sunflowers",
        "isHighlight": "true"
    }
    logger.info(f"Тест: Проверка запроса с некорректным типом. Данные: {query_data}")
    with pytest.raises(ValidationError):
        SearchQuery(**query_data, strict=True)
        logger.error(f"Ошибка: тип данных для поля 'isHighlight' некорректен, ожидался тип bool.")
