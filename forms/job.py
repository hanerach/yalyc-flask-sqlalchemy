from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired


class JobAddForm(FlaskForm):
    team_leader = IntegerField('Руководитель (id)', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Время на выполнение (в часах)', validators=[DataRequired()])
    collaborators = StringField('Коллабораторы (id через запятую)', validators=[DataRequired()])
    start_date = DateField('Начало работы')
    end_date = DateField('Конец работы')
    is_finished = BooleanField('Работа закончена?')

    submit = SubmitField('Применить')


