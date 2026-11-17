import pytest
import allure
import requests
import random

BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"

@pytest.fixture
def created_pet_id():
    pet_id = random.randint(100000, 999999)
    payload = {
        "id": pet_id,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200, f"Ошибка фикстуры: {response.text}"
    return pet_id