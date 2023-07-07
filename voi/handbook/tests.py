import pytest
from django.urls import reverse
from .models import HandbookScreenshot
# Create your tests here.

@pytest.mark.django_db
def test_should_delete_screenshot(
    client,
    upload_screenshot,
    send_new_user_access_token
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_screenshot",
        ),
        headers = send_new_user_access_token,
        data = upload_screenshot,
        format = 'json'
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_delete_screenshot(
    client,
    upload_screenshot,
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_screenshot",
        ),
        data = upload_screenshot,
        format = 'json'
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_field_empty_for_delete_screenshot(
    client,
    send_new_user_access_token
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_screenshot",
        ),
        headers = send_new_user_access_token,
        format = 'json'
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_screenshot_not_found_for_delete_screenshot(
    client,
    send_new_user_access_token
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_screenshot",
        ),
        headers = send_new_user_access_token,
        data = {"id": [999]},
        format = 'json'
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_responce_screenshot_already_delete_for_delete_screenshot(
    client,
    send_deleted_screenshot,
    send_new_user_access_token
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_screenshot",
        ),
        headers = send_new_user_access_token,
        data = send_deleted_screenshot,
        format = 'json'
    )

    assert responce.status_code == 400
    assert responce.data == {"error_screenshot_already_delete":"Screenshot already delete"}

@pytest.mark.django_db
def test_should_create_handbook(
    client,
    add_game,
    send_new_user_access_token,
    send_data_for_create_handbook,
):
        responce = client.post(
            reverse(    
                "handbook_api:create_handbook",
                kwargs={
                    "game_id": add_game.id
                }
            ),
            headers = send_new_user_access_token,
            data = send_data_for_create_handbook,
            format="json"
        )

        assert responce.status_code == 200

@pytest.mark.django_db
def test_should_respone_authorization_error_for_create_handbook(
    client,
    add_game,
    send_data_for_create_handbook,                
):
        responce = client.post(
            reverse(    
                "handbook_api:create_handbook",
                kwargs={
                    "game_id": add_game.id
                }
            ),
            data = send_data_for_create_handbook,
            format="json"
        )

        assert responce.status_code == 401

@pytest.mark.django_db
def test_should_respone_error_field_empty_for_create_handbook(
    client,
    add_game,
    send_new_user_access_token,
):
        responce = client.post(
            reverse(    
                "handbook_api:create_handbook",
                kwargs={
                    "game_id": add_game.id
                }
            ),
            headers = send_new_user_access_token,
            format="json"
        )

        assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_not_allowed_type_for_create_handbook(
    client,
    add_game,
    send_new_user_access_token,
    send_data_with_not_allowed_type_for_create_handbook,
):
        responce = client.post(
            reverse(    
                "handbook_api:create_handbook",
                kwargs={
                    "game_id": add_game.id
                }
            ),
            headers = send_new_user_access_token,
            data = send_data_with_not_allowed_type_for_create_handbook,
            format="json"
        )

        assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_game_not_found_for_create_handbook(
    client,
    send_new_user_access_token,
    send_data_for_create_handbook
):
        responce = client.post(
            reverse(    
                "handbook_api:create_handbook",
                kwargs={
                    "game_id": 999
                }
            ),
            headers = send_new_user_access_token,
            data = send_data_for_create_handbook,
            format="json"
        )

        assert responce.status_code == 404

@pytest.mark.django_db
def test_should_screenshot_upload(
    client,
    mocker,
    new_handbook,
    send_new_user_access_token,
    send_data_for_screenshot_upload
):
    mocker.patch.object(HandbookScreenshot.objects,'bulk_create', return_value="return Response({'status':'Upload'}, status=200)")
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

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_screenshot_upload(
    client,
    new_handbook,
    send_data_for_screenshot_upload
):
    responce = client.post(
        reverse(
            "handbook_api:screenshot_upload",
            kwargs={
                "handbook_id": new_handbook.id
            }
        ),
        data = {
                "file_url" : send_data_for_screenshot_upload
        }
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_field_empty_for_screenshot_upload(
    client,
    new_handbook,
    send_new_user_access_token,
):
    responce = client.post(
        reverse(
            "handbook_api:screenshot_upload",
            kwargs={
                "handbook_id": new_handbook.id
            }
        ),
        headers = send_new_user_access_token,
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_handbook_not_found_for_screenshot_upload(
    client,
    send_new_user_access_token,
    send_data_for_screenshot_upload
):
    responce = client.post(
        reverse(
            "handbook_api:screenshot_upload",
            kwargs={
                "handbook_id": 999
            }
        ),
        headers = send_new_user_access_token,
        data = {
                "file_url" : send_data_for_screenshot_upload
        }
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_responce_file_size_error_screenshot_upload(
    client,
    new_handbook,
    send_new_user_access_token,
    send_data_for_responce_file_size_error
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
                "file_url" : send_data_for_responce_file_size_error
        }
    )

    assert responce.status_code == 400
    assert responce.data == {"error_file_size": "File size is too large"}

@pytest.mark.django_db
def test_should_responce_file_ext_screenshot_upload(
    client,
    new_handbook,
    send_new_user_access_token,
    send_data_for_responce_file_ext_error
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
                "file_url" : send_data_for_responce_file_ext_error
        }
    )

    assert responce.status_code == 400
    assert responce.data == {"error_file_ext": "Invalid file type"}

@pytest.mark.django_db
def test_should_get_handbook_info(
    client,
    new_handbook,
):
    responce = client.get(
        reverse(
            "handbook_api:handbook_info",
            kwargs={
                "handbook_id": new_handbook.id
            }
        ),
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_handbook_not_found_for_handbook_info(
    client,
):
    responce = client.get(
        reverse(
            "handbook_api:handbook_info",
            kwargs={
                "handbook_id": 999
            }
        ),
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_edit_handbook(
    client,
    new_handbook,
    send_new_user_access_token,
    send_data_for_edit_handbook
):
    responce = client.put(
        reverse(
            "handbook_api:edit_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        headers = send_new_user_access_token,
        data = send_data_for_edit_handbook,
        format = 'json'
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_edit_handbook(
    client,
    new_handbook,
    send_data_for_edit_handbook
):
    responce = client.put(
        reverse(
            "handbook_api:edit_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        data = send_data_for_edit_handbook,
        format = 'json'
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_field_empty_error_for_edit_handbook(
    client,
    new_handbook,
    send_new_user_access_token,
):
    responce = client.put(
        reverse(
            "handbook_api:edit_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        headers = send_new_user_access_token,
        format = 'json'
    )

    assert responce.status_code == 400

@pytest.mark.django_db
def test_should_responce_handbook_not_found_error_for_edit_handbook(
    client,
    send_new_user_access_token,
    send_data_for_edit_handbook
):
    responce = client.put(
        reverse(
            "handbook_api:edit_handbook",
            kwargs={
                "handbook_id": 999
            },
        ),
        headers = send_new_user_access_token,
        data = send_data_for_edit_handbook,
        format = 'json'
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_responce_user_id_error_edit_handbook(
    client,
    new_handbook,
    send_new_user_access_token2,
    send_data_for_edit_handbook
):
    responce = client.put(
        reverse(
            "handbook_api:edit_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        headers = send_new_user_access_token2,
        data = send_data_for_edit_handbook,
        format = 'json'
    )

    assert responce.status_code == 403

@pytest.mark.django_db
def test_should_responce_type_not_allowed_error_for_edit_handbook(
    client,
    new_handbook,
    send_new_user_access_token,
    send_data_with_not_allowed_type_for_create_handbook
):
    responce = client.put(
        reverse(
            "handbook_api:edit_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        headers = send_new_user_access_token,
        data = send_data_with_not_allowed_type_for_create_handbook,
        format = 'json'
    )

    assert responce.status_code == 400
    assert responce.data == {"error_handbook_type_not_allowed": "Handbook type not allowed"}

@pytest.mark.django_db
def test_should_delete_handbook(
    client,
    new_handbook,
    send_new_user_access_token,
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        headers = send_new_user_access_token,
        format = 'json'
    )

    assert responce.status_code == 200

@pytest.mark.django_db
def test_should_responce_authorization_error_for_delete_handbook(
    client,
    new_handbook,
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        format = 'json'
    )

    assert responce.status_code == 401

@pytest.mark.django_db
def test_should_responce_handbook_not_found_error_for_delete_handbook(
    client,
    send_new_user_access_token,
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_handbook",
            kwargs={
                "handbook_id": 999
            },
        ),
        headers = send_new_user_access_token,
        format = 'json'
    )

    assert responce.status_code == 404

@pytest.mark.django_db
def test_should_responce_user_id_error_delete_handbook(
    client,
    new_handbook,
    send_new_user_access_token2,
):
    responce = client.delete(
        reverse(
            "handbook_api:delete_handbook",
            kwargs={
                "handbook_id": new_handbook.id
            },
        ),
        headers = send_new_user_access_token2,
        format = 'json'
    )

    assert responce.status_code == 403