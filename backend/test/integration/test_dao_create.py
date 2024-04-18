import unittest
from unittest.mock import patch
import pytest
from pymongo import MongoClient

from src.util.dao import DAO

test_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {
                "bsonType": "string",
                "description": "the first name of a user"
            }, 
            "lastName": {
                "bsonType": "string",
                "description": "the last name of a user"
            },
            "email": {
                "bsonType": "string",
                "description": "the email address of a user"
            }
        }
    }
}

@pytest.fixture(scope="session")
def test_db_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test_database']
    yield db

    client.drop_database('test_database')

@pytest.fixture()
def sut(test_db_connection):
    with patch("src.util.dao.getValidator") as mock_validator:
        mock_validator.return_value = test_validator
        dao = DAO("test")
 
        return dao

# Testing the create method
def test_create_user(sut):
    valid_data = {"firstName": "susm", "lastName": "susmen", "email": "susm@gmail.com"}
    result = sut.create(valid_data)
    assert result is not None
    assert result['firstName'] == 'susm'
    assert result['lastName'] == 'susmen'
    assert result['firstName'] is not 'Alle'

# Testing the to call on the wrong user
def test_create_call_wrong_user(sut):
    valid_data = {"firstName": "susm", "lastName": "susmen", "email": "susm@gmail.com"}
    result = sut.create(valid_data)
    assert result is not None
    with pytest.raises(Exception):
        assert result['firstName'] == 'Alle'

# Testing the create method twice
def test_create_user_two_users(sut):
    valid_data1 = {"firstName": "susm", "lastName": "susmen", "email": "susm@gmail.com"}
    valid_data2 = {"firstName": "Alle", "lastName": "Allen", "email": "alle@gmail.com"}
    result1 = sut.create(valid_data1)
    result2 = sut.create(valid_data2)
    assert result1 is not None
    assert result2 is not None
    assert result1['firstName'] == 'susm'
    assert result2['firstName'] == 'Alle'

# Testing inputting wrong format into dict
def test_create_wrong_user_format(sut):
    valid_data = {"firstName": "susm", "lastName": "susmen", "emailaddress": "susm@gmail.com"}
    with pytest.raises(Exception):
        sut.create(valid_data)

# Testing inputting empty dict
def test_create_empty_dict(sut):
    valid_data = {}
    with pytest.raises(Exception):
        sut.create(valid_data)

# Testing creating user with minimum properties
def test_create_minumum_properties(sut):
    valid_data = {"firstName": "Alle", "lastName": "", "email": ""}
    result = sut.create(valid_data)
    assert result is not None
