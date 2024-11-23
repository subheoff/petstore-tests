import pytest
import requests


# тест на получение наличия товара
def test_store_inventory(base_url):
    # запрос на получение наличия товара
    response = requests.get(f'{base_url}/store/inventory')
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    # проверка на наличие ключа available
    response_data = response.json()
    assert "available" in response_data, f"available не найден в {response_data}"


# тест на получение заказа по id
@pytest.mark.parametrize(
    "order_id",
    [
        1,
        2,
        3
    ]
)
def test_store_get_order(base_url, order_id):
    # запрос на получение
    response = requests.get(f'{base_url}/store/order/{order_id}')
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response_data = response.json()
    assert response_data["id"] == order_id, f"id заказа не совпадает"


# тест на создание заказа
def test_store_create_order(base_url):
    # данные и запрос на создание заказа
    order_data = {
        "id": 10,
        "petId": 10,
        "quantity": 1,
        "shipDate": "2024-11-22T00:00:00.000+0000",
        "status": "placed",
        "complete": True
    }

    response = requests.post(f"{base_url}/store/order", json=order_data)
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response_data = response.json()
    assert response_data["id"] == order_data["id"], 'id заказа не совпадают'
    assert response_data["petId"] == order_data["petId"], 'petId заказа не совпадают'
    assert response_data["quantity"] == order_data["quantity"], 'quantity заказа не совпадают'
    assert response_data["shipDate"] == order_data["shipDate"], 'shipDate заказа не совпадают'
    assert response_data["status"] == order_data["status"], 'status заказа не совпадают'
    assert response_data["complete"] == order_data["complete"], 'shipDate заказа не совпадают'


# тест удаление заказа
@pytest.mark.parametrize(
    "order_id",
    [
        1,
        2,
        3
    ]
)
def test_delete_order(base_url, order_id):
    # создаем заказ
    order_data = {
        "id": order_id,
        "petId": 10,
        "quantity": 1,
        "shipDate": "2024-11-22T00:00:00.000+0000",
        "status": "placed",
        "complete": True
    }

    response = requests.post(f"{base_url}/store/order", json=order_data)
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    # удаляем заказ
    response = requests.delete(f'{base_url}/store/order/{order_id}')
    assert response.status_code == 200, f"заказ {order_id} не удален"