import pytest
from django.urls import reverse
from .models import GameScreenshot
from voi.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
# Create your tests here.

@pytest.mark.django_db
def test_should_add_game(
        client,
        send_data_for_add_game,
        send_new_admin_user_access_token
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
        send_data_for_add_game,
        send_new_user_access_token
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
        send_new_admin_user_access_token
    ):

    responce = client.post(
        reverse("games_api:add_game"),
        headers = send_new_admin_user_access_token,
        data = None
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_screenshot_upload(
        client,
        mocker,
        add_game,
        send_data_for_screenshot_upload,
        send_new_admin_user_access_token
    ):
    mocker.patch.object(GameScreenshot.objects,'bulk_create', return_value="return Response({'status':'Upload'}, status=200)")
    responce = client.post(
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
def test_should_responce_isnt_admin_error_for_screenshot_upload(
        client,
        add_game,
        send_new_user_access_token,
        send_data_for_screenshot_upload
    ):

    responce = client.post(
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
def test_should_responce_authorization_error_for_screenshot_upload(
        client,
        add_game,
        send_data_for_screenshot_upload
    ):

    responce = client.post(
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
def test_should_responce_game_not_found_error_for_screenshot_upload(
        client,
        send_data_for_screenshot_upload,
        send_new_admin_user_access_token
    ):

    responce = client.post(
        reverse(
            "games_api:screenshot_upload",
            kwargs={
                "game_id": 99
            }
        ),
        headers = send_new_admin_user_access_token,
        data = {
                "file_url" : send_data_for_screenshot_upload
            }
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_field_empty_error(
        client,
        add_game,
        send_new_admin_user_access_token
    ):

    responce = client.post(
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
        mocker,
        add_game,
        send_new_admin_user_access_token,
        send_data_for_responce_file_size_error
    ):
    responce = client.post(
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
    assert responce.data == {"error_file_size": "File size is too large"}

@pytest.mark.django_db
def test_should_responce_file_ext_error(
        client,
        add_game,
        send_new_admin_user_access_token,
        send_data_for_responce_file_ext_error
    ):
    responce = client.post(
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
    assert responce.data == {"error_file_ext": "Invalid file type"}

@pytest.mark.django_db
def test_should_view_game_info(
        client,
        add_game,
    ):

    responce = client.get(
        reverse(
            "games_api:game_info",
            kwargs={
                "game_id": add_game.id
            }
        ),
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_game_not_found_error_for_game_info(
        client,
        add_game,
    ):

    responce = client.get(
        reverse(
            "games_api:game_info",
            kwargs={
                "game_id": 99
            }
        ),
    )

    assert responce.status_code == 404