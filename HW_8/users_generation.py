import random
import collections
from calendar import monthrange
from datetime import datetime

# в данном методе создаем случайную дату для дня рождения условного юзера
# с учетом разницы в количестве дней в месяце и с учетом високосных годов


def generate_date():
    year = random.randint(1980, 2005)
    month = random.randint(1, 12)
    n_days = monthrange(year, month)
    day = random.randint(1, n_days[1])

    date = datetime(year=year, month=month, day=day).date()

    return date


# создаем список словарей с данными тестовых пользователей вида [{'name':datetime(birthday)}}];
# словарь создаем на основании именованного кортежа и метода generate_date();

def generete_users():
    User = collections.namedtuple('User', ['name', 'birthday'])

    users_quantity = 1000
    users = []

    for i in range(users_quantity):
        user = User(f'name_{i}', generate_date())
        user_dict = dict(zip(user._fields, user[:]))
        users.append(user_dict)

    return users