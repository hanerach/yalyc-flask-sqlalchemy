from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Jobs
from data.reqparse_job import parser


def abort_if_news_not_found(job_id):  # вместо @app.errorhandler(404)
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        # Функция abort генерирует HTTP-ошибку с нужным кодом и возвращает ответ в формате JSON
        abort(404, message=f"News {job_id} not found")


# Для каждого ресурса (единица информации в REST называется ресурсом: новости, пользователи и т. д.) создается
# два класса: для одного объекта и для списка объектов: здесь это NewsResource и NewsListResource соответственно.

class UsersResource(Resource):
    def get(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date',
                  'is_finished'))})

    def delete(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    #     get и post - без аргументов.
    #     Доступ к данным, переданным в теле POST-запроса - парсинг аргументов (reqparse)


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date',
                  'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            colaborators=args['colaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})