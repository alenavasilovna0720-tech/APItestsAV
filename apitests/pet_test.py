
import allure
import requests
import random

BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"



@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistant_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содежимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"



    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self):
        pet_id = random.randint(100000, 999999)
        payload = {
            "id": pet_id,
            "name": "Buddy",
            "status": "available"
        }

        with allure.step("Создание питомца (подготовка данных)"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            assert response.status_code == 200, f"Ошибка создания: {response.text}"
        with allure.step("Получение информации о питомце"):
            get_response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert get_response.status_code == 200, f"Ожидали 200, получили {get_response.status_code}"
            data = get_response.json()
            assert data["id"] == pet_id, "Вернулся не тот питомец"




    @allure.title("Обновление информации о питомце")
    def test_update_pet_by_id(self):
        pet_id = random.randint(100000, 999999)
        payload = {
            "id": pet_id,
            "name": "Buddy",
            "status": "available"
        }

        with allure.step("Создание питомца (подготовка данных)"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            assert response.status_code == 200, f"Ошибка создания: {response.text}"
        update_payload = {
            "id": pet_id,
            "name": "Buddy Updated",
            "status": "sold"
        }
        with allure.step("Обновление информации о питомце"):
            put_response = requests.put(url=f"{BASE_URL}/pet", json=update_payload)
            assert put_response.status_code == 200, f"Ошибка обновления! Сервер ответил: {put_response.status_code}. Тело: {put_response.text}"
            data = put_response.json()
            assert data["id"] == pet_id, "Информация о питомце не обновилась"
            assert data["name"] == "Buddy Updated"
            assert data["status"] == "sold"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self):
        pet_id = random.randint(100000, 999999)
        payload = {
            "id": pet_id,
            "name": "Buddy",
            "status": "available"
        }

        with allure.step("Создание питомца (подготовка данных)"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            assert response.status_code == 200, f"Ошибка создания: {response.text}"

        with allure.step("Удаление питомца"):
            delete_response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

            assert delete_response.status_code == 200, f"Ошибка удаления: {delete_response.text}"

        with allure.step("Проверка, что питомец удален"):

            get_response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")


            assert get_response.status_code == 404, f"Питомец не удалился! Ответ: {get_response.text}"





    allure.title("Создание нового питомца")
    def test_add_pet(self):
        pet_id = random.randint(100000, 999999)
        payload = {
            "id": pet_id,
            "name": "doggie",
            "category": {
                "id": 1,
                "name": "Dogs"
            },
            "photoUrls": ["string"],
            "tags":[
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "available"
        }
        with allure.step("Отправка POST-запроса с полными данными"):
            post_response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            assert post_response.status_code == 200, f"Ошибка: {post_response.text}"
        with allure.step("Проверка, что ответ содержит все переданные данные"):
            data = post_response.json()
            assert data["id"] == pet_id
            assert data["name"] == "doggie"
            assert data["category"]["name"] == "Dogs"
            assert data["photoUrls"] == ["string"]
            assert data["tags"] == [{"id": 0, "name": "string"}]



    @allure.title("Получение списка питомцев по статусу")
    def test_find_pets_by_status (self, created_pet_id):
       with allure.step("Получение списка питомцев по статусу 'available'"):
           get_response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": "available"})
           assert get_response.status_code == 200, f"ошибка {get_response.status_code}"
           data = get_response.json()
           assert isinstance(data, list), "Ответ сервера не является списком"
           pet_ids = [pet["id"] for pet in data]
           assert created_pet_id in pet_ids, "Созданного питомца нет в списке со статусом available!"









