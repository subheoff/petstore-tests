import pytest
import requests


# фикстура для создания питомца
@pytest.fixture
def create_pet(base_url):
    def _create_pet(pet_id, name="no_name", status="available", category_name="not_defined", photo_urls=None, tags=None):
        if photo_urls is None:
            photo_urls = ["string"]
        if tags is None:
            tags = [{"id": 0, "name": "string"}]

        pet_data = {
            "id": pet_id,
            "category": {
                "id": 0,
                "name": category_name
            },
            "name": name,
            "photoUrls": photo_urls,
            "tags": tags,
            "status": status
        }

        response = requests.post(f"{base_url}/pet", json=pet_data)
        assert response.status_code == 200, f"питомец не создан: {response.text}"

        return pet_data

    return _create_pet


# фикстура для удаления питомца
@pytest.fixture
def delete_pet(base_url):
    def _delete_pet(pet_id):
        response = requests.delete(f"{base_url}/pet/{pet_id}")
        print(response.json())
        assert response.status_code == 200, f"питомец не удален: {response.text}"
    return _delete_pet


# тест на проверку создания питомца и проверку переданных данных
@pytest.mark.parametrize(
    "pet_id, name, status, category_name, photo_urls, tags",
    [
        (101, "Busya", "available", "dogs", ["https://example.com/busya.jpg"], [{"id": 1, "name": "cute"}]),
        (102, "Koshka", "pending", "cats", ["https://example.com/koshka.jpg"], None),
        (103, "Kesha", "sold", "birds", None, [{"id": 3, "name": "fast"}]),
    ]
)
def test_create_and_get_pet(base_url, create_pet, pet_id, name, status, category_name, photo_urls, tags):
    # создаем питомца
    pet_data = create_pet(pet_id, name, status, category_name, photo_urls, tags)

    # делаем запрос к питомцу
    response = requests.get(f"{base_url}/pet/{pet_data['id']}")
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response_data = response.json()
    assert response_data["id"] == pet_data["id"], "id питомца не совпадает"
    assert response_data["name"] == pet_data["name"], "name питомца не совпадает"
    assert response_data["status"] == pet_data["status"], "status питомца не совпадает"
    assert response_data["category"]["name"] == pet_data["category"]["name"], "category_name питомца не совпадает"
    assert response_data["photoUrls"] == pet_data["photoUrls"], "photoUrls питомца не совпадают"
    assert response_data["tags"] == pet_data["tags"], "tags питомца не совпадают"


# тест на обновление данных питомца и проверку переданных данных
@pytest.mark.parametrize(
    "pet_id, name, status, photo_urls, tags",
    [
        (201, "Busya", "available", ["https://example.com/busya.jpg"], [{"id": 1, "name": "cute"}]),
        (202, "Koshka", "pending", ["https://example.com/koshka.jpg"], None),
        (203, "Kesha", "sold", None, [{"id": 3, "name": "fast"}]),
    ]
)
def test_update_pet(base_url, create_pet, pet_id, name, status, photo_urls, tags):
    # создаем питомца
    create_pet(pet_id=pet_id)

    # запрос на обновление данных
    updated_pet_data = {
        "id": pet_id,
        "name": name,
        "photoUrls": photo_urls,
        "tags": tags,
        "status": status
    }
    response = requests.put(f"{base_url}/pet", json=updated_pet_data)
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response_data = response.json()
    assert response_data["id"] == pet_id, "id не обновилось"
    assert response_data["name"] == name, "name не обновился"
    assert response_data["status"] == status, "status не обновился"
    if photo_urls:
        assert response_data["photoUrls"] == photo_urls, "photoUrls не обновился"
    if tags:
        assert response_data["tags"] == tags, "tags не обновились"


# тест на удаление питомца
def test_delete_pet(base_url, create_pet, delete_pet):
    pet_id = 301
    # создаем питомца
    create_pet(pet_id)

    # удаляем питомца
    delete_pet(pet_id)

    response = requests.get(f"{base_url}/pet/{pet_id}")
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"


# тест на поиск питомца по статусу
@pytest.mark.parametrize(
    "status",
    [
        "available",
        "pending",
        "sold",
    ]
)
def test_find_by_status(base_url, status):

    response = requests.get(f"{base_url}/pet/findByStatus?status={status}")
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response_data = response.json()
    for i in response_data:
        assert i["status"] == status, f"{i["status"]} не является {status}"