import pprint
from requests import get, post, delete
import datetime

print(delete('http://localhost:5000/api/jobs/2').json())
print(delete('http://localhost:5000/api/jobs/999').json()) # новости с id = 999 нет в базе
print(delete('http://localhost:5000/api/jobs/10').json()) # новости с id = 10 нет в базе
pprint.pprint(get('http://localhost:5000/api/jobs').json())




