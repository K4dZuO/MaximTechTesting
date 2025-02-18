import pytest
import requests
from pydantic import ValidationError


from models import Objects


BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"


@pytest.fixture(params=['', '?departmentIds=1', '?metadataDate=2020-01-01'])
def api_response(request):
    """Фикстура, делающая запрос к API и возвращающая объект ответа."""
    url = f"{BASE_URL}{request.param}"
    response = requests.get(url)
    return response


def test_get_objects_status(api_response):
    """Проверяем статус ответа."""
    assert api_response.status_code == 200, f"Статус-код: {api_response.status_code}"


def test_get_objects_validation(api_response):
    """Проверяем соответствие модели Pydantic."""
    try:
        objects_data = Objects.model_validate(api_response.json())
    except ValidationError as e:
        pytest.fail(f"Ошибки валидации модели Objects: {e}")


def test_total_is_int(api_response):
    """Проверяем, что total — это целое число."""
    objects_data = Objects.model_validate(api_response.json())
    assert isinstance(objects_data.total, int), "Поле total должно быть целым числом"


def test_objectIDs_is_list(api_response):
    """Проверяем, что objectIDs — это список."""
    objects_data = Objects.model_validate(api_response.json())
    assert isinstance(objects_data.objectIDs, list), "Поле objectIDs должно быть списком"


def test_objectIDs_contains_ints(api_response):
    """Проверяем, что все элементы objectIDs являются целыми числами."""
    objects_data = Objects.model_validate(api_response.json())
    assert all(isinstance(id, int) for id in objects_data.objectIDs), "В objectIDs должны быть только int"

def test_empty_objectIDs_when_total_zero(api_response):
    """Если total = 0, то objectIDs должен быть пустым."""
    objects_data = Objects.model_validate(api_response.json())
    if objects_data.total == 0:
        assert objects_data.objectIDs == [], "Если total = 0, то objectIDs должен быть пустым"


@pytest.mark.parametrize("invalid_department", [-1, 99999])
def test_invalid_department(invalid_department):
    """Проверяем, что API корректно обрабатывает несуществующие департаменты."""
    response = requests.get(f"{BASE_URL}?departmentIds={invalid_department}")
    assert response.status_code == 200, f"Ожидался 200, но получен {response.status_code}"
    
    try:
        objects_data = Objects.model_validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Ответ API не прошел валидацию: {e}")

    assert objects_data.total == 0, "Ожидалось total = 0 для несуществующего департамента"
    assert objects_data.objectIDs == [], "Ожидался пустой список objectIDs"
