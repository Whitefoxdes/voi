import pytest
from .models import User, ImageProfile, Profile
from django.urls import reverse
from voi.settings import BASE_DIR
# Create your tests here.

@pytest.mark.django_db
def test_should_register_user(
        client,
        mocker,
        send_data_for_register_user
    ):
    mocker.patch("django.core.mail.send_mail", return_value="return Response({'status':'Register'}, status=200)")
    responce = client.post(
        reverse("user_api:register"),
        send_data_for_register_user
    )
    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_user_serializer_error_for_register(
        client,
        send_data_for_user_serializer_error
    ):

    responce = client.post(
        reverse("user_api:register"),
        send_data_for_user_serializer_error
    )
    
    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_profile_serializer_error_for_register(
        client,
        send_data_for_profile_serializer_error
    ):

    responce = client.post(
        reverse("user_api:register"),
        send_data_for_profile_serializer_error
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_email_exist_error_for_register(
        client,
        send_data_with_exist_email
    ):

    responce = client.post(
        reverse("user_api:register"),
        send_data_with_exist_email
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_activate_user(
        client,
        new_user
    ):

    responce = client.put(
        reverse(
        "user_api:activate_user",
        kwargs={
            "user_activation_uuid": new_user.user_activation_uuid
        }
        )
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_activated_user_error(
        client,    
        send_data_with_activated_user
    ):

    responce = client.put(
        reverse(
        "user_api:activate_user",
        kwargs={
            "user_activation_uuid": send_data_with_activated_user.user_activation_uuid
        }
        )
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_login_user(
        client,
        send_data_for_login_new_user
    ):

    responce = client.post(
        reverse("user_api:login"),
        send_data_for_login_new_user
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_unactivated_user_error(
        client,
        send_data_for_login_user_with_unactivated_user
    ):

    responce = client.post(
        reverse("user_api:login"),
        send_data_for_login_user_with_unactivated_user
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_user_serializer_error_for_login(
        client,
    ):
    
    responce = client.post(
        reverse("user_api:login"),
        data = None
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_get_user_profile(
        client,
        send_new_user_access_token
    ):

    responce = client.get(
        reverse("user_api:user_profile"),
        headers = send_new_user_access_token
    )
    
    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_user_profile(
        client,
    ):

    responce = client.get(
        reverse("user_api:user_profile"),
        headers = None
    )
    
    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_edit_email(
        client,
        send_data_for_edit_email,
        send_new_user_access_token
    ):

    responce = client.put(
        reverse("user_api:edit_email"),
        headers = send_new_user_access_token,
        data = send_data_for_edit_email
    )
    
    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_edit_email(
        client,
        send_data_for_edit_email
    ):

    responce = client.put(
        reverse("user_api:edit_email"),
        headers = None,
        data = send_data_for_edit_email
    )
    
    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_user_serializer_error_for_edit_email(
        client,
        send_new_user_access_token
    ):

    responce = client.put(
        reverse("user_api:edit_email"),
        headers = send_new_user_access_token,
        data = None
    )
    
    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_email_exits_error_for_edit_email(
        client,
        send_new_user_access_token,
        send_data_for_edit_email_with_exist_email
    ):

    responce = client.put(
        reverse("user_api:edit_email"),
        headers = send_new_user_access_token,
        data = send_data_for_edit_email_with_exist_email
    )
    
    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_wrong_password_error_for_edit_email(
        client,
        send_new_user_access_token,
        send_data_for_edit_email_with_wrong_password
    ):

    responce = client.put(
        reverse("user_api:edit_email"),
        headers = send_new_user_access_token,
        data = send_data_for_edit_email_with_wrong_password
    )
    
    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_change_password(
        client,
        mocker,
        send_new_user_access_token,
        send_data_for_change_password
    ):
    
    mocker.patch("django.core.mail.send_mail", return_value="return Response({'status':'Update'}, status=200)")
    responce = client.put(
        reverse("user_api:change_password"),
        headers = send_new_user_access_token,
        data = send_data_for_change_password
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_change_password(
        client,
        send_data_for_change_password
    ):

    responce = client.put(
        reverse("user_api:change_password"),
        headers = None,
        data = send_data_for_change_password
    )
    
    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_wrong_old_password_for_change_password(
        client,
        send_new_user_access_token,
        send_data_for_change_password_with_wrong_old_password
    ):

    responce = client.put(
        reverse("user_api:change_password"),
        headers = send_new_user_access_token,
        data = send_data_for_change_password_with_wrong_old_password
    )
    
    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_user_serializer_error_for_change_password(
        client,
        send_new_user_access_token,
        send_data_with_only_old_password
    ):

    responce = client.put(
        reverse("user_api:change_password"),
        headers = send_new_user_access_token,
        data = send_data_with_only_old_password
    )
    
    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_edit_profile(
        client,
        send_new_user_access_token,
        send_data_for_edit_profile
    ):

    responce = client.put(
        reverse("user_api:edit_profile"),
        headers = send_new_user_access_token,
        data = send_data_for_edit_profile
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_edit_profile(
        client,
        send_data_for_edit_profile
    ):

    responce = client.put(
        reverse("user_api:change_password"),
        headers = None,
        data = send_data_for_edit_profile
    )
    
    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_profile_serializer_error_for_edit_profile(
        client,
        send_new_user_access_token
    ):

    responce = client.put(
        reverse("user_api:change_password"),
        headers = send_new_user_access_token,
        data = None
    )
    
    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_send_reset_password_letter(
        client,
        mocker,
        send_data_for_send_reset_password_letter
    ):
    mocker.patch("django.core.mail.send_mail", return_value="return Response({'status':'Send'}, status=200)")
    responce = client.post(
        reverse("user_api:send_reset_password_letter"),
        data = send_data_for_send_reset_password_letter
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_send_reset_password_letter_serializer_error(
        client,
    ):

    responce = client.post(
        reverse("user_api:send_reset_password_letter"),
        data = None
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_email_not_found_error(
        client,
        send_data_for_email_not_found_error
    ):

    responce = client.post(
        reverse("user_api:send_reset_password_letter"),
        data = send_data_for_email_not_found_error
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_reset_password(
        client,
        send_data_for_reset_password,
        new_user
    ):

    responce = client.put(
        reverse(
            "user_api:reset_password",
            kwargs={
                "reset_password_uuid": new_user.reset_password_uuid
            }
        ),
        data = send_data_for_reset_password
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_reset_password_serializer_error(
        client,
        new_user
    ):

    responce = client.put(
        reverse(
            "user_api:reset_password",
            kwargs={
                "reset_password_uuid": new_user.reset_password_uuid
            }
        ),
        data = None
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_url_incapacitated_error(
        client,
        send_data_for_reset_password,
    ):

    responce = client.put(
        reverse(
            "user_api:reset_password",
            kwargs={
                "reset_password_uuid": None
            }
        ),
        data = send_data_for_reset_password
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_user_avatar_upload(
        client,
        mocker,
        send_new_user_access_token
    ):

    mocker.patch.object(Profile, "save", return_value="return Response({'status':'Upload'}, status=200)")
    mocker.patch.object(ImageProfile, "save", return_value="return Response({'status':'Upload'}, status=200)")
    
    responce = client.put(
        reverse("user_api:user_avatar_upload"),
        headers = send_new_user_access_token,
        data = {
            "file_url": (BASE_DIR / "media" / "for_test" / "test.png").open("rb")
        }
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_file_upload(
        client,
    ):

    responce = client.put(
        reverse("user_api:user_avatar_upload"),
        headers = None,
        data = {
            "file_url": (BASE_DIR / "media" / "for_test" / "test.png").open("rb")
        }
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_file_size_error(
        client,
        send_new_user_access_token
    ):

    responce = client.put(
        reverse("user_api:user_avatar_upload"),
        headers = send_new_user_access_token,
        data = {
            "file_url": (BASE_DIR / "media" / "for_test" / "test2.txt").open("rb")
        }
    )

    assert responce.status_code == 400
    assert responce.data == {"error_file_size": "File size is too large"}

@pytest.mark.django_db
def test_should_responce_file_ext_error(
        client,
        send_new_user_access_token
    ):

    responce = client.put(
        reverse("user_api:user_avatar_upload"),
        headers = send_new_user_access_token,
        data = {
            "file_url": (BASE_DIR / "media" / "for_test" / "test3.txt").open("rb")
        }
    )

    assert responce.status_code == 400
    assert responce.data == {"error_file_ext": "Invalid file type"}