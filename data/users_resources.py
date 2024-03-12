from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.users import User
from data.reqparse_user import parser

from werkzeug.security import generate_password_hash


def set_password(password):
    return generate_password_hash(password)


def abort_if_news_not_found(user_id):  # вместо @app.errorhandler(404)
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        # Функция abort генерирует HTTP-ошибку с нужным кодом и возвращает ответ в формате JSON
        abort(404, message=f"User {user_id} not found")


# Для каждого ресурса (единица информации в REST называется ресурсом: новости, пользователи и т. д.) создается
# два класса: для одного объекта и для списка объектов: здесь это NewsResource и NewsListResource соответственно.

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address',
                  'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    #     get и post - без аргументов.
    #     Доступ к данным, переданным в теле POST-запроса - парсинг аргументов (reqparse)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address',
                  'email', 'hashed_password')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=set_password(args['hashed_password'])
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})