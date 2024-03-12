from requests import get, post, delete

# print(get('http://localhost:5000/api/v2/users').json())
# print(get('http://localhost:5000/api/v2/users/1').json())
# print(get('http://localhost:5000/api/v2/users/52').json())  # нет такой новости
# print(get('http://localhost:5000/api/v2/users/q').json())  # не число

# print(post('http://localhost:5000/api/v2/users').json())  # нет словаря
# print(post('http://localhost:5000/api/v2/users', json={'title': 'Sonya'}).json())  # не все поля
# print(post('http://localhost:5000/api/v2/users', json={'surname': 'TEST SURNAME',
#                                                        'name': 'TEST NAME',
#                                                        'age': 222,
#                                                        'position': 'test_pos',
#                                                        'speciality': 'test_spec',
#                                                        'address': 'test_address',
#                                                        'email': 'test_email@email.com',
#                                                        'hashed_password': 'test'}).json())
#
# print(delete('http://localhost:5000/api/v2/users/999').json())  # id = 999 нет в базе
# print(delete('http://localhost:5000/api/v2/users/1').json())
