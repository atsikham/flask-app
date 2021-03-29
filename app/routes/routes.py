from app.common.common import error_handler
from app.models.user import User
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask import current_app as app
from flask import jsonify, request, Response


@app.route('/health', methods=['GET'])
def health_check():
    return Response('', status=200, mimetype='application/json')


@app.route('/hello/<username>', methods=['PUT'])
@error_handler
def add_or_update_user(username):
    request_data = request.get_json()
    User.add_or_replace_user(username, **request_data)
    return Response('', status=204, mimetype='application/json')


@app.route('/hello/<username>', methods=['GET'])
@error_handler
def get_user(username):
    user = User.get_user(username)
    birthday = datetime.strptime(user.birthday, '%Y-%m-%d').date()
    today = date.today()
    year_diff = today.year - birthday.year
    next = birthday + relativedelta(years=year_diff)
    if next < today:
        next = next + relativedelta(years=1)

    day_diff = (next - today).days
    if day_diff == 0:
        response = jsonify({'message': f'Hello, {username}! Happy birthday!'})
    else:
        response = jsonify({'message': f'Hello, {username}! Your birthday is in {day_diff} day(s)'})
    return response
