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


def test_status_code():
    """Тестирует, что запрос возвращает успешный код состояния (200)."""
    objectID = 45734  # Пример objectID
    logger.info(f"Тест: Проверка кода состояния для objectID {objectID}")
    response = requests.get(f"{BASE_URL}/{objectID}")
    
    if response.status_code == 200:
        logger.info(f"Ответ: успешный код состояния 200 для objectID {objectID}")
    else:
        logger.error(f"Ошибка: ожидаемый код состояния 200, но получен {response.status_code}")
    
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


def test_valid_object_data():
    """Проверка того, что данные объекта правильные (например, объект с ID 45734)."""
    objectID = 45734
    logger.info(f"Тест: Проверка данных для объекта с ID {objectID}")
    response = requests.get(f"{BASE_URL}/{objectID}")
    data = response.json()
    
    # Проверяем, что объект возвращает нужные ключи
    missing_keys = [key for key in ["objectID", "title", "primaryImage", "artistDisplayName"] if key not in data]
    if missing_keys:
        logger.error(f"Ошибка: отсутствуют ключи: {missing_keys}")
    else:
        logger.info("Все обязательные ключи присутствуют в ответе.")
    
    # Дополнительно проверяем данные
    assert "objectID" in data, "objectID is missing"
    assert "title" in data, "title is missing"
    assert "primaryImage" in data, "primaryImage is missing"
    assert "artistDisplayName" in data, "artistDisplayName is missing"
    
    # Проверяем, что objectID совпадает
    if data["objectID"] == objectID:
        logger.info(f"objectID совпадает: {data['objectID']}")
    else:
        logger.error(f"Ошибка: ожидался objectID {objectID}, но получен {data['objectID']}")
    
    # Проверяем имя художника
    if "Kiyohara Yukinobu" in data["artistDisplayName"]:
        logger.info(f"Имя художника совпадает с ожидаемым: {data['artistDisplayName']}")
    else:
        logger.error(f"Ошибка: ожидаемое имя художника 'Kiyohara Yukinobu', но получено {data['artistDisplayName']}")


def test_is_public_domain():
    """Тестирует, что объект находится в общественном достоянии (если доступно)."""
    objectID = 45734
    logger.info(f"Тест: Проверка общественного достояния для объекта с ID {objectID}")
    response = requests.get(f"{BASE_URL}/{objectID}")
    data = response.json()
    
    if "isPublicDomain" in data:
        if data["isPublicDomain"]:
            logger.info(f"Объект с ID {objectID} находится в общественном достоянии.")
        else:
            logger.error(f"Ошибка: объект с ID {objectID} не является общественным достоянием.")
    else:
        logger.error(f"Ошибка: отсутствует информация о публичном достоянии для объекта с ID {objectID}")
    
    # Проверяем, что объект находится в общественном достоянии
    assert "isPublicDomain" in data, "isPublicDomain is missing"
    assert data["isPublicDomain"] is True, f"Expected 'isPublicDomain' to be True, but got {data['isPublicDomain']}"


def test_image_urls():
    """Проверка, что объект возвращает изображения в правильном формате."""
    objectID = 45734
    logger.info(f"Тест: Проверка изображений для объекта с ID {objectID}")
    response = requests.get(f"{BASE_URL}/{objectID}")
    data = response.json()
    
    # Проверка основной картинки и дополнительных
    if "primaryImage" in data:
        if data["primaryImage"].startswith("https://images.metmuseum.org/"):
            logger.info(f"Основная картинка URL верный: {data['primaryImage']}")
        else:
            logger.error(f"Ошибка: основная картинка URL неверный: {data['primaryImage']}")
    else:
        logger.error("Ошибка: отсутствует основная картинка.")
    
    if "additionalImages" in data:
        for img_url in data["additionalImages"]:
            if img_url.startswith("https://images.metmuseum.org/"):
                logger.info(f"Дополнительное изображение URL верный: {img_url}")
            else:
                logger.error(f"Ошибка: дополнительное изображение URL неверный: {img_url}")


def test_invalid_objectID():
    """Проверка обработки несуществующего objectID."""
    objectID = 99999999  # Некорректный ID
    logger.info(f"Тест: Проверка для несуществующего objectID {objectID}")
    response = requests.get(f"{BASE_URL}/{objectID}")
    
    if response.status_code == 404:
        logger.info(f"Ошибка: objectID {objectID} не найден, код состояния 404.")
    else:
        logger.error(f"Ошибка: ожидался код состояния 404 для несуществующего objectID, но получен {response.status_code}")
    
    assert response.status_code == 404, f"Expected status code 404 for invalid ID, but got {response.status_code}"
