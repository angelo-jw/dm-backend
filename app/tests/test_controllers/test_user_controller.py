import app.controllers.user as user_controller


def test__create_user__returns_user__when_user_does_not_exist(test_user, db_session):
    created_user = user_controller.create_user(test_user)

    assert created_user['email'] == test_user['email']
