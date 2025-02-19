# Python Test Open API

Этот проект включает тесты для работы с Open API (методами, связанными с департаментами и объектами). Тесты написаны с использованием `pytest` и проверяют корректность работы API.

## Запуск тестов

Для запуска тестов выполните следующие команды:

```python
pytest -v ./tests/test_departments.py
pytest -v ./tests/test_objects.py
pytest -v ./tests/test_object.py
pytest -v ./tests/test_search.py
```