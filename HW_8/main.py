import collections
from datetime import datetime, timedelta
from users_generation import generete_users


# основной метод, в котором создаем график поздравлений на ближайшую неделю

def create_congrats_shedule(users):
    # создаем список с ближайшими 7 датами (на неделю вперед), начиная с сегодняшнего дня
    # (сегдняшний исключаем)
    current_date = datetime.now().date()
    next_week_dates = [current_date + timedelta(days=i) for i in range(1, 8)]

    # создаем дефолтный словарь, в который будем добавлять пары
    # {'День недели':[список имен юзеров для поздравления]}
    users_to_congrat = collections.defaultdict(list)

    # перебираем все даты ближайшей недели
    for date in next_week_dates:
        for user in users:
            # перебираем пользователей в списке пользователей и сравниваем даты их рождения
            # с датами ближайшей недели
            if user['birthday'].month == date.month and user['birthday'].day == date.day:
                # берем строчное представление дня недели рассматриваемой даты
                weekday = date.strftime('%A')
                # если ДР выпадает на выходной, то имя добавляем в список понедельника
                if datetime.weekday(date) in [5, 6]:
                    users_to_congrat['Monday'].append(user['name'])
                else:
                    users_to_congrat[weekday].append(user['name'])

    return users_to_congrat


# красиво выводим результат


def print_results(users_to_congrat):
    for key, val in users_to_congrat.items():
        values = ', '.join(list(val))
        print('{:>10}: {:<100}'.format(key, values))


# вызываем основные методы


def main():
    users = generete_users()
    users_to_congrat = create_congrats_shedule(users)
    print_results(users_to_congrat)


# задаем точку входа
if __name__ == '__main__':
    main()
