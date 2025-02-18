import pytest
import requests
from pydantic import ValidationError
from models import Departments, DepartmentRow

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"

@pytest.fixture
def api_response():
    """Фикстура, делающая запрос к API и возвращающая объект ответа."""
    response = requests.get(BASE_URL)
    return response

@pytest.fixture
def valid_department():
    """Пример валидного департамента"""
    return {"departmentId": 1, "displayName": "American Decorative Arts"}

@pytest.fixture
def invalid_department():
    """Пример невалидного департамента"""
    return {"departmentId": "abc", "displayName": None}  # Ошибки типов

def test_valid_data(api_response):
    """Проверяем, что API-ответ проходит валидацию Pydantic"""
    try:
        Departments.model_validate(api_response.json())
    except ValidationError as e:
        pytest.fail(f"Ошибка валидации: {e}")

def test_invalid_department(invalid_department):
    """Проверяем, что неверные данные вызывают ошибку"""
    with pytest.raises(ValidationError):
        DepartmentRow.model_validate(invalid_department)

def test_department_fields(valid_department):
    """Проверяем правильность полей модели"""
    department = DepartmentRow.model_validate(valid_department)
    
    assert department.departmentId == 1, "departmentId должен быть 1"
    assert department.displayName == "American Decorative Arts", "Название отдела некорректно"