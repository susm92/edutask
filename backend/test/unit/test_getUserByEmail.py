import pytest
from unittest.mock import MagicMock, patch
from src.controllers.usercontroller import UserController
from src.util.dao import DAO


class TestUserController:
    @patch.object(DAO, 'find')
    def test_get_user_by_email_valid(self, mock_find):
        # Mocking the DAO
        mock_dao = MagicMock(spec=DAO)
        #Creating the Usercontroller with the mocked DAO
        user_controller = UserController(dao=mock_dao)

        # Mocking the data for the test
        mock_email = "existing@gmail.com"
        mock_user = {"email": mock_email, "name": "Test User"}

        # setting the return value
        mock_dao.find.return_value = [mock_user]
        # calling the method to get a result
        result = user_controller.get_user_by_email(mock_email)
        # comparing the resutl with the mocked user
        assert result == mock_user
        mock_dao.find.assert_called_once_with({'email': mock_email})

    @patch.object(DAO, 'find')
    def test_get_user_by_email_multiple_users(self, mock_find):
        # Mocking the DAO
        mock_dao = MagicMock(spec=DAO)
        #Creating the Usercontroller with the mocked DAO
        user_controller = UserController(dao=mock_dao)
        # Mocking the data for the test
        mock_email = "multipleusers@gmail.com"
        mock_user1 = {"email": mock_email, "name": "Alle"}
        mock_user2 = {"email": mock_email, "name": "Susm"}
        mock_user3 = {"email": mock_email, "name": "Person3"}

        # setting the return value for all three
        mock_dao.find.return_value = [mock_user1, mock_user2, mock_user3]
        # calling the method to get a result
        result = user_controller.get_user_by_email(mock_email)

        # comparing the result with the first mocked user
        assert result == mock_user1
        mock_dao.find.assert_called_once_with({'email': mock_email})

    @patch.object(DAO, 'find')
    def test_get_user_by_email_no_user(self, mock_find):
        # This test fails because the ground truth says that the method should return "None"
        # if the email does not exist
        # However, the code never returns "None" and instead tries to return "user[0]"
        # resulting in an IndexError

        # Mocking the DAO
        mock_dao = MagicMock(spec=DAO)
        #Creating the Usercontroller with the mocked DAO
        user_controller = UserController(dao=mock_dao)

        # Mocking the data for the test
        mock_email = "nonexistent@gmail.com"
        # setting the retrn value
        mock_dao.find.return_value = []
        # calling the function with the mocked email
        result = user_controller.get_user_by_email(mock_email)

        # checking that the result is None
        assert result is None
        mock_dao.find.assert_called_once_with({'email': mock_email})

    @patch.object(DAO, 'find')
    def test_get_user_by_email_invalid_email(self, mock_find):
        # Mocking the DAO
        mock_dao = MagicMock(spec=DAO)
        #Creating the Usercontroller with the mocked DAO
        user_controller = UserController(dao=mock_dao)

        # Mocking the data for the test
        mock_email = "weirdandnotworkingemail.com"

        # calling the method with the mocked email and asserting that Valueerror is raised
        with pytest.raises(ValueError):
            user_controller.get_user_by_email(mock_email)

    def test_get_user_by_email_no_mocked_dao(self):
        # Mocking the DAO
        user_controller = UserController(dao=None)

        # Mocking the data for the test
        mock_email = "nodatabase@gmail.com"

        # calling the method with the mockd email and asserting that it raises an exception
        with pytest.raises(Exception):
            user_controller.get_user_by_email(mock_email)

