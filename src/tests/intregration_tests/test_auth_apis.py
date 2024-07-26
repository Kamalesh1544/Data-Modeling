from src.test.intregration_tests.test_main import client


def test_get_user_api():
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"v1/users/{user_id}")

    print(response.json())

    assert response.status_code == 200  # noqa
    user_data = response.json()
    data = user_data["data"]
    assert data["user_id"] == user_id
    assert data["fullname"] == "testuser"
    assert data["email"] == "testuser@example.com"


# def test_get_user_not_found():
#     with patch("src.app.db.models.user.user_model.UserTable.get",
#                side_effect=Exception("User not found")):
#         user_id = "nonexistent-uuid"
#         response = client.get(f"v1/users/{user_id}")
#         assert response.status_code == 404
