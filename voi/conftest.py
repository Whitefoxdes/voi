import pytest
from uuid import uuid4
from user.models import (
    User,
    Profile
)
from games.models import (
    Games,
    GameScreenshot
)
from handbook.models import (
    Handbook,
    HandbookType,
    HandbookScreenshot
)
from django.urls import reverse
from voi.settings import BASE_DIR
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password

@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def new_user() -> None:

    new_profile = Profile(
        username = "tester",
        date_of_birth = "2000-01-01"
    )
    new_profile.save()

    new_user = User(
        email = "tester@email.com",
        password = make_password("password"),
        profile = new_profile,
        user_activation_uuid = uuid4()
    )
    new_user.save()
    return new_user

@pytest.fixture
def send_data_for_register_user() -> None:
    data = {
        "email":"test@email.com",
        "password":"password",
        "username":"tester",
        "date_of_birth":"2000-01-01"
    }

    return data

@pytest.fixture
def send_data_for_user_serializer_error() -> None:
    data = {
        "email":"",
        "password":"",
        "username":"tester",
        "date_of_birth":"2000-01-01"
    }

    return data

@pytest.fixture
def send_data_for_profile_serializer_error() -> None:
    data = {
        "email":"test@email.com",
        "password":"password",
        "username":"",
        "date_of_birth":""
    }
    return data

@pytest.fixture
def send_data_with_exist_email(new_user) -> None:
    data = {
        "email":new_user.email,
        "password":"password",
        "username":"tester",
        "date_of_birth":"2000-01-01"
    }

    return data

@pytest.fixture
def send_data_with_activated_user(new_user) -> None:
    new_user.is_active = True
    new_user.save()
    return new_user

@pytest.fixture
def send_data_for_login_new_user(new_user) -> None:
    new_user.is_active = True
    new_user.save()
    data = {
        "email": new_user.email,
        "password":"password",
    }

    return data

@pytest.fixture
def send_data_for_login_user_with_unactivated_user(new_user) -> None:
    data = {
        "email": new_user.email,
        "password":"password",
    }

    return data

@pytest.fixture
def send_new_user_obtain_token(client, send_data_for_login_new_user) -> None:
    responce = client.post(
        reverse("user_api:login"),
        send_data_for_login_new_user
    )

    return responce.data

@pytest.fixture
def send_new_user_access_token(send_new_user_obtain_token) -> None:

    access_token = send_new_user_obtain_token["access"]

    authorization = {"Authorization": f"Bearer {access_token}"}

    return authorization

@pytest.fixture
def send_data_for_edit_email() -> None:

    data = {
        "email": "tester2@email.com",
        "password":"password",
    }

    return data

@pytest.fixture
def send_data_for_edit_email_with_exist_email(client, new_user) -> None:

    data = {
        "email": new_user.email,
        "password":"password",
    }

    return data

@pytest.fixture
def send_data_for_edit_email_with_wrong_password(client, new_user) -> None:

    data = {
        "email": "tester@email.com",
        "password":"password2",
    }

    return data

@pytest.fixture
def send_data_for_change_password(client, new_user) -> None:

    data = {
        "email": "tester@email.com",
        "old_password": "password",
        "password": "password2",
    }

    return data

@pytest.fixture
def send_data_for_change_password_with_wrong_old_password(client, new_user) -> None:

    data = {
        "email": "tester@email.com",
        "old_password": "password2",
        "password":"password2",
    }

    return data

@pytest.fixture
def send_data_for_change_password_with_wrong_old_password(client, new_user) -> None:

    data = {
        "email": "tester@email.com",
        "old_password": "password2",
        "password":"password2",
    }

    return data

@pytest.fixture
def send_data_with_only_old_password(client, new_user) -> None:

    data = {
        "old_password": "password"
    }

    return data

@pytest.fixture
def send_data_for_edit_profile() -> None:

    data = {
        "username": "tester2",
        "date_of_birth":"2000-01-02",
    }

    return data

@pytest.fixture
def send_data_for_send_reset_password_letter(new_user):
    data = {
        "email": new_user.email
    }

    return data

@pytest.fixture
def send_data_for_email_not_found_error():
    data = {
        "email": "testerN@email.com"
    }

    return data

@pytest.fixture
def send_data_for_reset_password(new_user):
    
    new_user.reset_password_uuid = uuid4()
    new_user.save()

    reset_password_uuid = new_user.reset_password_uuid

    data = {
        "password": "password2",
    }

    return data

@pytest.fixture
def new_admin_user(new_user):
    new_user.is_admin = True
    new_user.is_staff = True
    new_user.save()
    return new_user

@pytest.fixture
def send_data_for_login_new_admin_user(new_admin_user):
    new_admin_user.is_active = True
    new_admin_user.save()
    data = {
        "email": new_admin_user.email,
        "password":"password",
    }

    return data

@pytest.fixture
def send_new_admin_user_obtain_token(client, send_data_for_login_new_admin_user):
    responce = client.post(
        reverse("user_api:login"),
        send_data_for_login_new_admin_user
    )

    return responce.data

@pytest.fixture
def send_new_admin_user_access_token(send_new_admin_user_obtain_token):
    access_token = send_new_admin_user_obtain_token["access"]

    authorization = {"Authorization": f"Bearer {access_token}"}

    return authorization    

@pytest.fixture
def send_data_for_add_game():
    data = {
        "name" : "test_game"
    }
    return data

@pytest.fixture
def add_game():
    add_game = Games(
        name = "test_game",
        is_active = True
    )
    add_game.save()
    return add_game

@pytest.fixture
def send_data_for_add_game_with_exist_game_name(add_game):
    data = {
        "name" : add_game.name
    }
    return data

@pytest.fixture
def send_data_for_screenshot_upload():
    data = [
        (BASE_DIR / "media" / "for_test" / "test.png").open("rb"),
        (BASE_DIR / "media" / "for_test" / "test.png").open("rb"),
        (BASE_DIR / "media" / "for_test" / "test.png").open("rb")
    ]
    return data

@pytest.fixture
def send_data_for_responce_file_size_error():
    data = [
        (BASE_DIR / "media" / "for_test" / "test.png").open("rb"),
        (BASE_DIR / "media" / "for_test" / "test2.txt").open("rb"),
        (BASE_DIR / "media" / "for_test" / "test.png").open("rb")
    ]
    return data

@pytest.fixture
def send_data_for_responce_file_ext_error():
    data = [
        (BASE_DIR / "media" / "for_test" / "test.png").open("rb"),
        (BASE_DIR / "media" / "for_test" / "test3.txt").open("rb"),
        (BASE_DIR / "media" / "for_test" / "test.png").open("rb")
    ]
    return data

@pytest.fixture
def add_handbook_type():
    type = HandbookType(
        type_name="BESTIARIES"
    )
    type.save()
    return type

@pytest.fixture
def send_data_for_create_handbook(add_handbook_type):
    data = {
        "title": "test",
        "body": "test",
        "type": {
            "id": add_handbook_type.id,
            "type_name": add_handbook_type.type_name
        }
    }
    return data

@pytest.fixture
def send_data_with_not_allowed_type_for_create_handbook(add_handbook_type):
    data = {
        "title": "test",
        "body": "test",
        "type": {
            "id": 999,
            "type_name": "TEST"
        }
    }
    return data

@pytest.fixture
def new_handbook(
    new_user,
    add_game,
    add_handbook_type
):
    
    new_handbook = Handbook(
        title="Test",
        body="Test",
        author=new_user,
        game=add_game,
        type=add_handbook_type
    )
    new_handbook.save()

    return new_handbook

@pytest.fixture
def send_data_for_edit_handbook(add_handbook_type):
    data = {
        "title": "test 2",
        "body": "test 2",
        "type": {
            "id": add_handbook_type.id,
            "type_name": add_handbook_type.type_name
        }
    }

    return data

@pytest.fixture
def new_user2():

    new_profile = Profile(
        username = "tester",
        date_of_birth = "2000-01-01"
    )
    new_profile.save()

    new_user = User(
        email = "tester2@email.com",
        password = make_password("password"),
        profile = new_profile,
        user_activation_uuid = uuid4()
    )
    new_user.save()
    return new_user

@pytest.fixture
def send_data_for_login_new_user2(new_user2):
    new_user2.is_active = True
    new_user2.save()
    data = {
        "email": new_user2.email,
        "password":"password",
    }

    return data
@pytest.fixture
def send_new_user_obtain_token2(client, send_data_for_login_new_user2):
    responce = client.post(
        reverse("user_api:login"),
        send_data_for_login_new_user2
    )

    return responce.data

@pytest.fixture
def send_new_user_access_token2(send_new_user_obtain_token2):

    access_token = send_new_user_obtain_token2["access"]

    authorization = {"Authorization": f"Bearer {access_token}"}

    return authorization

@pytest.fixture
def upload_screenshot(
    client,
    new_handbook,
    send_new_user_access_token,
    send_data_for_screenshot_upload
):
    responce = client.post(
        reverse(
            "handbook_api:screenshot_upload",
            kwargs={
                "handbook_id": new_handbook.id
            }
        ),
        headers = send_new_user_access_token,
        data = {
                "file_url" : send_data_for_screenshot_upload
        }
    )
    return {"id": [1, 2, 3]}

@pytest.fixture
def send_deleted_screenshot(
    upload_screenshot
):
        deleted_screenshot = HandbookScreenshot.objects.filter(pk=upload_screenshot["id"][0]).first()
        deleted_screenshot.is_delete = True
        deleted_screenshot.save()
        return {"id" : [deleted_screenshot.id]}