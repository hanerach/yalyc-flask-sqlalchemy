import flask
# Согласно архитектуре REST, обмен данными между клиентом и сервером осуществляется в формате JSON (реже — XML).
# Поэтому формат ответа сервера flask изменён с помощью метода jsonify, который преобразует наши данные в JSON.
from flask import request, jsonify

from . import db_session
from .jobs import Jobs

# Механизм разделения приложения Flask на независимые модули
# Как правило, blueprint — логически выделяемый набор обработчиков адресов.
# Blueprint работает аналогично объекту приложения Flask, но в действительности он не является приложением.
blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify(
        {'jobs': [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                     'start_date', 'end_date', 'is_finished')) for item in jobs]})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    # Согласно REST, далее нужно реализовать получение информации об одной новости. Фактически, мы уже получили из списка
    # всю информацию о каждой новости. При проектировании приложений по архитектуре REST обычно поступают таким образом:
    # когда возвращается список объектов, он содержит только краткую информацию (например, только id и заголовок)...
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    # ...а полную информацию (текст и автора) можно посмотреть с помощью запроса, который мы обработаем далее.
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify({'jobs': jobs.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                               'start_date', 'end_date', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    # Проверив, что запрос содержит все требуемые поля, мы заносим новую запись в базу данных.
    # request.json содержит тело запроса, с ним можно работать, как со словарем.
    db_sess = db_session.create_session()

    job = Jobs(
        id = request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['POST'])
def edit_job(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    # Проверив, что запрос содержит все требуемые поля, мы заносим новую запись в базу данных.
    # request.json содержит тело запроса, с ним можно работать, как со словарем.
    db_sess = db_session.create_session()

    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )


    job_to_edit = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not job_to_edit:
        return jsonify({'error': 'Not found'})
    job_to_edit.id = job.id
    job_to_edit.job = job.job
    job_to_edit.team_leader = job.team_leader
    job_to_edit.work_size = job.work_size
    job_to_edit.collaborators = job.collaborators
    job_to_edit.start_date = job.start_date
    job_to_edit.end_date = job.end_date
    job_to_edit.is_finished = job.is_finished

    db_sess.commit()
    return jsonify({'success': 'OK'})