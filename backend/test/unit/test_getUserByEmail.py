import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

class MockDAO:
    def __init__(self, users):
        self.users = users
    
    def find(self, query):
        return [user for user in self.users if user['email'] == query['email']]

class TestUserController:
    @pytest.mark.unit
    def test_get_user_by_email_invalid_email(self):
        mock_dao = Mock(spec=MockDAO)
        
        user_controller = UserController(mock_dao)
        
        # Sending an invalid email address
        with pytest.raises(ValueError) as exc_info:
            user_controller.get_user_by_email('should not work')

        # Asserting that ValueError is raised due to invalid email address sent
        assert str(exc_info.value) == 'Error: invalid email address'

    @pytest.mark.unit
    def test_get_user_by_email_no_user(self):
        mock_dao = Mock(spec=MockDAO)
        mock_dao.find.return_value = []
        
        user_controller = UserController(mock_dao)
        
        # Trying to get user while sending an email that does not exist, expecting index error
        #with pytest.raises(IndexError):
        
        # This has been changed, we should get None and not an error as before!
        assert user_controller.get_user_by_email('nonexistent@email.com') == None

    @pytest.mark.unit
    def test_get_user_by_email_invalid_email_type_int(self):
        mock_dao = Mock(spec=MockDAO)
        
        user_controller = UserController(mock_dao)
        
        # Trying to get user by email while sending an integer, wrong type, expecting string
        with pytest.raises(TypeError):
            user_controller.get_user_by_email(123)
    
    @pytest.mark.unit
    def test_get_user_by_email_invalid_email_type_list(self):
        mock_dao = Mock(spec=MockDAO)
        
        user_controller = UserController(mock_dao)
        
        # Trying to get user by email while sending a list of integers, wrong type, expecting string
        with pytest.raises(TypeError):
            user_controller.get_user_by_email([1,2,3])
