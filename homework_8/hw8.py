# ЗАДАНИЕ №1
from datetime import datetime
#
# def time_cheker(my_obj):
#     def timer_func(*args, **kwargs):
#         res = my_obj(*args, **kwargs)
#         res_addr = hex(id(res)) # адрес памяти экземпляра класса
#         f = open("add_object_class.txt", "a", encoding="UTF-8")
#         current_datetime = datetime.now()
#         f.writelines(f'{current_datetime.strftime("%d-%m-%Y %H:%M")} Создан экземпляр класса {my_obj.__name__} по адресу памяти {res_addr} \n')
#         f.close()
#         return res
#
#     return timer_func
#
#
# @time_cheker
# class Departments:
#
#     def __init__(self, dep_name):
#         self.dep_name = dep_name
#
#     def __str__(self):
#         return self.dep_name
#
# dep = Departments("Test1")
# dep2 = Departments("Test2")
# dep3 = Departments("Test3")
# print(dep)
# print(dep2)
# print(dep3)

# Задание №2
# 2. На основе прошлых ДЗ необходимо создать модели представлений для классов ДЕПАРТАМЕНТЫ (Departments),
# СОТРУДНИКИ (Employees), ЗАЯВКИ (Orders). Реализовать магические методы вывода информации на экран как для пользователя,
# так и для "машинного" отображения.
#
#
# Предусмотреть все необходимые ограничения и связи моделей между собой.
#
#
# У каждой модели предусмотрите метод, который бы мог осуществлять запись хранимой в экземпляре информации в отдельный
# json-файл с именем вида <id записи>.json. Если id не существует - выдавать ошибку.



# import json
#
# products = {
#     'Onion': {
#         'price': 12,
#         'in_stock': 1000,
#         'description': 'Лук'
#     },
#     'Tomato': {
#         'price': 4,
#         'in_stock': 10000,
#         'description': 'Помидоры'
#     },
#     'Cucumber': {
#         'price': 10,
#         'in_stock': 500,
#         'description': 'Огурцы',
#         # 'test' : {1, 2, 3}
#     }
# }
#
# json_object = json.dumps(products)
# print(json_object)
# print(type(json_object))
#
# with open("products_data.json", "w", encoding="UTF-8") as json_f:
#     json.dump(products, json_f)




