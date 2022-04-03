import collections
from datetime import datetime, timedelta
from users_generation import generete_users


# основной метод, в котором создаем график поздравлений на ближайшую неделю

def create_congrats_shedule(users):
    # создаем список с ближайшими 7 датами (на неделю вперед), начиная с сегодняшнего дня
    # (сегдняшний исключаем)
    current_date = datetime.now().date()
    next_week_dates = [current_date + timedelta(days=i) for i in range(1, 8)]
    # смотрим, какая дата в нашем 7-дневном календаре максимальная, чтобы потом проверить,
    # не является ли Сб или Вс последними в нашем календаре; если являются, тогда мы не переносим
    # поздравления на след. неделю (на новый понедельник)
    max_date = max(next_week_dates)

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
                weekday_num = datetime.weekday(date)

                # если ДР выпадает на выходной в начале или середине календаря,
                # то имя добавляем в список понедельника; если ДР выпадает на выходной в конце календаря,
                # то не добавляем в список поздравлений
                if weekday_num in [5, 6] and date < max_date - timedelta(days=1):
                    users_to_congrat['Monday'].append(user['name'])
                elif weekday_num in [5, 6] and date >= max_date - timedelta(days=1):
                    continue
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
