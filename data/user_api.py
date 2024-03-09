import flask
# Согласно архитектуре REST, обмен данными между клиентом и сервером осуществляется в формате JSON (реже — XML).
# Поэтому формат ответа сервера flask изменён с помощью метода jsonify, который преобразует наши данные в JSON.
from flask import request, jsonify

from . import db_session
from .users import User

# Механизм разделения приложения Flask на независимые модули
# Как правило, blueprint — логически выделяемый набор обработчиков адресов.
# Blueprint работает аналогично объекту приложения Flask, но в действительности он не является приложением.
blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify(
        {'users': [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                      'speciality', 'address', 'email',
                                      'hashed_password', 'modified_date')) for item in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    # Согласно REST, далее нужно реализовать получение информации об одной новости. Фактически, мы уже получили из списка
    # всю информацию о каждой новости. При проектировании приложений по архитектуре REST обычно поступают таким образом:
    # когда возвращается список объектов, он содержит только краткую информацию (например, только id и заголовок)...
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    # ...а полную информацию (текст и автора) можно посмотреть с помощью запроса, который мы обработаем далее.
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify({'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                               'speciality', 'address', 'email',
                                               'hashed_password', 'modified_date'))})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email',
                  'hashed_password', 'modified_date']):
        return jsonify({'error': 'Bad request'})
    # Проверив, что запрос содержит все требуемые поля, мы заносим новую запись в базу данных.
    # request.json содержит тело запроса, с ним можно работать, как со словарем.
    db_sess = db_session.create_session()

    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
        modidied_date=request.json['modidied_date']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
        modidied_date=request.json['modidied_date']
    )

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
