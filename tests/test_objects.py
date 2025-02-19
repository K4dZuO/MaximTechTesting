import pytest
import requests
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"


@pytest.fixture(params=[
    45734,    
    3,        
    9999999   # Несуществующий ID
])
def object_response(request):
    """Фикстура для тестирования разных objectID"""
    object_id = request.param
    url = f"{BASE_URL}/{object_id}"
    logger.info(f"Запрос к API с objectID: {object_id}")
    response = requests.get(url)
    return response, object_id


def test_object_response_status(object_response):
    """Проверка статус-кодов ответов"""
    response, object_id = object_response
    
    if object_id == 9999999:
        logger.info(f"Тест: проверка для несуществующего objectID {object_id}")
        assert response.status_code == 404, "Несуществующий objectID должен возвращать 404"
        logger.info(f"Ответ: получен код состояния 404 для несуществующего objectID {object_id}")
    else:
        logger.info(f"Тест: проверка для валидного objectID {object_id}")
        assert response.status_code == 200, "Валидные objectID должны возвращать 200 OK"
        logger.info(f"Ответ: получен код состояния 200 OK для objectID {object_id}")


def test_object_data_structure(object_response):
    """Проверка структуры данных в ответе"""
    response, object_id = object_response
    
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Проверка структуры данных для objectID {object_id}: {data}")
        
        # Проверяем основные ключи
        assert "objectID" in data, "Ключ 'objectID' отсутствует"
        assert "title" in data, "Ключ 'title' отсутствует"
        assert "primaryImage" in data, "Ключ 'primaryImage' отсутствует"
        assert "artistDisplayName" in data, "Ключ 'artistDisplayName' отсутствует"
        
        logger.info(f"Структура данных для objectID {object_id} прошла проверку.")


def test_object_is_public_domain(object_response):
    """Проверка, что объект находится в общественном достоянии (если доступно)"""
    response, object_id = object_response
    
    if response.status_code == 200:
        data = response.json()
        
        if "isPublicDomain" in data:
            assert isinstance(data["isPublicDomain"], bool), "Поле 'isPublicDomain' должно быть булевым"
            logger.info(f"Проверка поля 'isPublicDomain' для objectID {object_id}: {data['isPublicDomain']}")
        else:
            logger.warning(f"Поле 'isPublicDomain' отсутствует для objectID {object_id}")


def test_object_image_url(object_response):
    """Проверка правильности URL изображения"""
    response, object_id = object_response
    
    if response.status_code == 200:
        data = response.json()
        
        if "primaryImage" in data and data["primaryImage"]:
            assert data["primaryImage"].startswith("https://images.metmuseum.org/"), "URL основного изображения некорректен"
            logger.info(f"Проверка URL основного изображения для objectID {object_id}: {data['primaryImage']}")
        else:
            logger.warning(f"Основное изображение отсутствует или пустое для objectID {object_id}")


def test_multiple_objectID_responses():
    """Тестирование нескольких objectID на корректные ответы"""
    object_ids = [45734, 3, 9999999]
    
    for object_id in object_ids:
        url = f"{BASE_URL}/{object_id}"
        logger.info(f"Запрос к API для objectID {object_id}")
        response = requests.get(url)
        
        if object_id == 9999999:
            assert response.status_code == 404, f"Несуществующий objectID {object_id} должен возвращать 404"
            logger.info(f"Ответ для objectID {object_id}: получен статус 404")
        else:
            assert response.status_code == 200, f"Валидный objectID {object_id} должен возвращать 200 OK"
            logger.info(f"Ответ для objectID {object_id}: получен статус 200 OK")


def test_object_additional_images(object_response):
    """Проверка наличия дополнительных изображений"""
    response, object_id = object_response
    
    if response.status_code == 200:
        data = response.json()
        
        if "additionalImages" in data:
            for img_url in data["additionalImages"]:
                assert img_url.startswith("https://images.metmuseum.org/"), f"Некорректный URL для изображения {img_url}"
                logger.info(f"Дополнительное изображение для objectID {object_id}: {img_url}")
        else:
            logger.warning(f"Дополнительные изображения отсутствуют для objectID {object_id}")
