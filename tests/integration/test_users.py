import json
import os
import pytest

from app import create_app, db
from app.models.user import User
from datetime import date
from dateutil.relativedelta import relativedelta


@pytest.fixture(scope='module')
def test_cases_positive():
    return [
        {
            'username': 'Testgetone',
            'delta_days': 170
        },
        {
            'username': 'Testgettwo',
            'delta_days': 285
        },
        {
            'username': 'Testgetthree',
            'delta_days': 0
        },
        {
            'username': 'Testputone',
            'delta_days': 8
        }
    ]


@pytest.fixture(scope='module')
def test_headers():
    return {
        'Content-Type': 'application/json'
    }


@pytest.fixture(scope='module')
def test_client(test_cases_positive):
    flask_app = create_app(db_uri='sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'test.db'))

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            db.create_all()
            for user_data in test_cases_positive:
                user = user_data['username']
                delta_days = user_data['delta_days']
                db.session.add(
                    User(name=user, birthday=date.today() + relativedelta(days=delta_days) - relativedelta(years=20)))
            db.session.commit()
            yield testing_client
            db.session.remove()
            db.drop_all()


def test_get_existing_this_year(test_client, test_cases_positive):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (GET)
    THEN check that the response is valid
    """
    user = test_cases_positive[0]['username']
    delta_days = test_cases_positive[0]['delta_days']
    response = test_client.get(f'/hello/{user}')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == f'Hello, {user}! Your birthday is in {delta_days} day(s)'


def test_get_existing_next_year(test_client, test_cases_positive):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (GET)
    THEN check that the response is valid
    """
    user = test_cases_positive[1]['username']
    delta_days = test_cases_positive[1]['delta_days']
    response = test_client.get(f'/hello/{user}')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == f'Hello, {user}! Your birthday is in {delta_days} day(s)'


def test_get_existing_today(test_client, test_cases_positive):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (GET)
    THEN check that the response is valid
    """
    user = test_cases_positive[2]['username']
    response = test_client.get(f'/hello/{user}')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == f'Hello, {user}! Happy birthday!'


def test_get_not_existing(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (GET) and there is no such user
    THEN check that the response is negative
    """
    response = test_client.get('/hello/fake')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'No such user found'


def test_put_correct_not_existing(test_client, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) and there was no such user
    THEN check that the response is valid and user created
    """
    data = {"dateOfBirth": "1995-04-08"}
    user = 'atsikham'
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 204
    response = test_client.get(f'/hello/{user}')
    assert f'Hello, {user}! Your birthday is in' in json.loads(response.data)['message']


def test_put_correct_existing(test_client, test_cases_positive, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) and there is such user already exists
    THEN check that the response is valid and user updated
    """
    data = {"dateOfBirth": "1995-04-08"}
    user = test_cases_positive[3]['username']
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 204


def test_put_correct_feb29(test_client, test_cases_positive, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) with correct February 29th date
    THEN check that the response is valid
    """
    data = {"dateOfBirth": "2020-02-29"}
    user = test_cases_positive[3]['username']
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 204


def test_put_incorrect_value_not_existing_date(test_client, test_cases_positive, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) with incorrect birthday value
    THEN check that the response is negative
    """
    data = {"dateOfBirth": "2021-02-29"}
    user = test_cases_positive[3]['username']
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Incorrect value passed'


def test_put_incorrect_value_future_date(test_client, test_cases_positive, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) with birthday in future
    THEN check that the response is negative
    """
    data = {"dateOfBirth": "2999-02-28"}
    user = test_cases_positive[3]['username']
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Incorrect value passed'


def test_put_incorrect_value_user(test_client, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) name that contains numbers
    THEN check that the response is negative
    """
    data = {"dateOfBirth": "2000-02-28"}
    user = 'atsikham123'
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Incorrect value passed'


def test_put_incorrect_new_field(test_client, test_cases_positive, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) with additional data field
    THEN check that the response is negative
    """
    data = {"dateOfBirth": "2021-02-29", 'key': 'value'}
    user = test_cases_positive[3]['username']
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 400
    assert 'unexpected keyword argument' in json.loads(response.data)['error']


def test_put_incorrect_missing_field(test_client, test_cases_positive, test_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/hello/<username>' page is requested (PUT) with missing required data field
    THEN check that the response is negative
    """
    data = {}
    user = test_cases_positive[3]['username']
    response = test_client.put(f'/hello/{user}', data=json.dumps(data), headers=test_headers)
    assert response.status_code == 400
    assert 'required positional argument' in json.loads(response.data)['error']
