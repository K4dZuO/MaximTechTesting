import pytest
import requests
from pydantic import ValidationError
import logging


from models import Departments, DepartmentRow


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"


@pytest.fixture
def api_response():
    """Фикстура, делающая запрос к API и возвращающая объект ответа."""
    logger.info("Отправка запроса к API для получения департаментов...")
    response = requests.get(BASE_URL)
    logger.info(f"Ответ получен с кодом: {response.status_code}")
    return response


@pytest.fixture
def valid_department():
    """Пример валидного департамента"""
    return {"departmentId": 1, "displayName": "American Decorative Arts"}


@pytest.fixture
def invalid_department():
    """Пример невалидного департамента"""
    return {"departmentId": "abc", "displayName": None} 


def test_valid_data(api_response):
    """Проверяем, что API-ответ проходит валидацию Pydantic"""
    logger.info("Проверка данных API на соответствие модели Departments...")
    try:
        Departments.model_validate(api_response.json())
        logger.info("Данные прошли валидацию успешно.")
    except ValidationError as e:
        logger.error(f"Ошибка валидации: {e}")
        pytest.fail(f"Ошибка валидации: {e}")


def test_invalid_department(invalid_department):
    """Проверяем, что неверные данные вызывают ошибку"""
    logger.info("Проверка обработки невалидного департамента...")
    with pytest.raises(ValidationError):
        DepartmentRow.model_validate(invalid_department)
    logger.info("Ошибка валидации для невалидного департамента была успешно вызвана.")


def test_department_fields(valid_department):
    """Проверяем правильность полей модели"""
    logger.info("Проверка правильности полей валидного департамента...")
    department = DepartmentRow.model_validate(valid_department)
    
    assert department.departmentId == 1, "departmentId должен быть 1"
    logger.info("departmentId проверен успешно.")
    
    assert department.displayName == "American Decorative Arts", "Название отдела некорректно"
    logger.info("Название отдела проверено успешно.")
