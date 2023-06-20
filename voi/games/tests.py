import pytest
from django.urls import reverse
from django.test import TestCase
# Create your tests here.

@pytest.mark.django_db
def test_should_add_game(
    client,
    send_new_admin_user_access_token,
    send_data_for_add_game
    ):

    responce = client.post(
        reverse("games_api:add_game"),
        headers = send_new_admin_user_access_token,
        data = send_data_for_add_game
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_isnt_admin_error_for_add_game(
    client,
    send_new_user_access_token,
    send_data_for_add_game
    ):

    responce = client.post(
        reverse("games_api:add_game"),
        headers = send_new_user_access_token,
        data = send_data_for_add_game
    )

    assert responce.status_code == 403

@pytest.mark.django_db
def test_should_responce_authorization_error_for_add_game(
    client,
    send_data_for_add_game
    ):

    responce = client.post(
        reverse("games_api:add_game"),
        headers = None,
        data = send_data_for_add_game
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_request_field_error_for_add_game(
    client,
    send_data_for_add_game,
    send_new_admin_user_access_token
    ):

    responce = client.post(
        reverse("games_api:add_game"),
        headers = send_new_admin_user_access_token,
        data = None
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_request_field_error_for_add_game(
    client,
    send_new_admin_user_access_token,
    send_data_for_add_game_with_exist_game_name
    ):

    responce = client.post(
        reverse("games_api:add_game"),
        headers = send_new_admin_user_access_token,
        data = send_data_for_add_game_with_exist_game_name
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_screenshot_upload(
    client,
    add_game,
    send_data_for_screenshot_upload,
    send_new_admin_user_access_token
    ):

    responce = client.put(
        reverse(
            "games_api:screenshot_upload",
            kwargs={
                "game_id": add_game.id
            }
        ),
        headers = send_new_admin_user_access_token,
        data = {
                "file_url" : send_data_for_screenshot_upload
            }
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_isnt_admin_error(
    client,
    add_game,
    send_new_user_access_token,
    send_data_for_screenshot_upload
    ):

    responce = client.put(
        reverse(
            "games_api:screenshot_upload",
            kwargs={
                "game_id": add_game.id
            }
        ),
        headers = send_new_user_access_token,
        data = {
                "file_url" : send_data_for_screenshot_upload
            }
    )

    assert responce.status_code == 403

@pytest.mark.django_db
def test_should_responce_authorization_error(
    client,
    add_game,
    send_data_for_screenshot_upload
    ):

    responce = client.put(
        reverse(
            "games_api:screenshot_upload",
            kwargs={
                "game_id": add_game.id
            }
        ),
        headers = None,
        data = {
                "file_url" : send_data_for_screenshot_upload
            }
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_field_empty_error(
    client,
    add_game,
    send_new_admin_user_access_token
    ):

    responce = client.put(
        reverse(
            "games_api:screenshot_upload",
            kwargs={
                "game_id": add_game.id
            }
        ),
        headers = send_new_admin_user_access_token,
        data = None
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_file_size_error(
    client,
    add_game,
    send_data_for_responce_file_size_error,
    send_new_admin_user_access_token
    ):

    responce = client.put(
        reverse(
            "games_api:screenshot_upload",
            kwargs={
                "game_id": add_game.id
            }
        ),
        headers = send_new_admin_user_access_token,
        data = {
                "file_url" : send_data_for_responce_file_size_error
            }
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_file_ext_error(
    client,
    add_game,
    send_data_for_responce_file_ext_error,
    send_new_admin_user_access_token
    ):

    responce = client.put(
        reverse(
            "games_api:screenshot_upload",
            kwargs={
                "game_id": add_game.id
            }
        ),
        headers = send_new_admin_user_access_token,
        data = {
                "file_url" : send_data_for_responce_file_ext_error
            }
    )

    assert responce.status_code == 400
