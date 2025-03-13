import pytest
import requests


@pytest.fixture
def create_user(base_url):
    def _create_user(user_id, username="user", firstname="no_name", lastname="no_name", email="example@mail.com", password="qwerty", phone="77777777777", userstatus=0):
        user_data = {
            "id": user_id,
            "username": username,
            "firstName": firstname,
            "lastName": lastname,
            "email": email,
            "password": password,
            "phone": phone,
            "userstatus": userstatus
        }

        response = requests.post(f"{base_url}/user", json=user_data)
        assert response.status_code == 200, f"user не создан: {response.text}"

        return user_data

    return _create_user


@pytest.mark.parametrize(
    "user_id, username, firstname, lastname",
    [
        (101, "user_anna", "Anna", "Smith"),
        (102, "user_bella", "Bella", None),
        (103, "user_jonh", None, "Smith"),
    ]
)
def test_get_user_by_username(base_url, create_user, user_id, username, firstname, lastname):
    user_data = create_user(user_id, username, firstname, lastname)

    response = requests.get(f"{base_url}/user/{username}")
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response_data = response.json()
    assert response_data["id"] == user_data["id"], "id не совпадают"
    if firstname:
        assert response_data["firstName"] == user_data["firstName"], "firstName не совпадают"
    if lastname:
        assert response_data["lastName"] == user_data["lastName"], "lastName не совпадают"


@pytest.mark.parametrize(
    "user_id, username, password",
    [
        (201, "user_anna", "qwerty1"),
        (202, "user_bella", "qwerty2"),
        (203, "user_jonh", "qwerty3"),
    ]
)
def test_login_user(base_url, create_user, user_id, username, password):
    create_user(user_id, username, password)

    response = requests.get(f"{base_url}/user/login", params={"username": username, "password": password})
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    assert "logged in user session" in response.text, "в логине отказано"


def test_logout_user(base_url, create_user):
    user_id = 301
    username = "logout_test"
    password = "qwerty"
    
    create_user(user_id, username, password)

    response = requests.get(f"{base_url}/user/login", params={"username": username, "password": password})
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response = requests.get(f"{base_url}/user/logout")
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"


@pytest.mark.parametrize(
    "user_id, username, updated_email, updated_phone",
    [
        (401, "update_test_user", "newemail1@mail.com", "123456789"),
        (402, "update_test_user2", "newemail2@mail.com", "987654321"),
        (403, "update_test_user3", "newemail3@mail.com", "555555555"),
    ]
)
def test_update_user(base_url, create_user, user_id, username, updated_email, updated_phone):
    user_data = create_user(user_id, username)

    updated_data = {
        "id": user_id,
        "username": username,
        "firstName": user_data["firstName"],
        "lastName": user_data["lastName"],
        "email": updated_email,
        "password": user_data["password"],
        "phone": updated_phone,
        "userstatus": user_data["userstatus"]
    }
    response = requests.put(f"{base_url}/user/{username}", json=updated_data)
    assert response.status_code == 200, f"данные не обновились: {response.text}"

    response = requests.get(f"{base_url}/user/{username}")
    assert response.status_code == 200, f"код {response.status_code}, {response.text}"

    response_data = response.json()
    assert response_data["email"] == updated_email, "email не обновлён"
    assert response_data["phone"] == updated_phone, "email не обновлён"


@pytest.mark.parametrize(
    "user_id, username",
    [
        (401, "delete_test_user1"),
        (402, "delete_test_user2"),
        (403, "delete_test_user3"),
    ]
)
def test_delete_user(base_url, create_user, user_id, username):
    create_user(user_id, username)

    response = requests.delete(f"{base_url}/user/{username}")
    assert response.status_code == 200, f"ошибка удаления: {response.text}"

    response = requests.get(f"{base_url}/user/{username}")
    assert response.status_code == 404, f"юзер не удален: {response.text}"
