import sys
import time
import sqlite3
from datetime import date

#
# # !!! Нельзя наследоваться от класса, у которого есть декоратор !!! Нарушение принципов ООП, т.к. в классе теперь лежит функция
#
# secret_password = "1234"
# current_password = sys.argv[1] #введённый пароль
#
# # Декоратор
# def check_password(f):
#     def inner(*args, **kwargs):
#         if secret_password == current_password:
#             return f(*args, **kwargs)
#         else:
#             raise Exception("Wrong password!")
#     return inner
#
#
# @check_password
# class Test():
#
#
#     def __init__(self, name):
#         self.name = name
#
# # t1 = Test("Nykodiuk")
# # print(t1)
#
#
# def time_cheker(my_obj):
#     def timer_func(*args, **kwargs):
#         print("Начало выполнения.")
#         st_time = time.time()
#         time.sleep(1)
#         my_obj(*args, **kwargs)
#         end_time = ("%s second" % (time.time() - st_time))
#         print("Конец выполнения.")
#         print(f'Время выполнения {my_obj}: {end_time} \n')
#     return timer_func
#
#
# p1 = Test("Nykodiuk")
# print(p1)
#
#
# print("Начинаю работать")
# # Получения аргументом из терминала с помощью команды sys.argv
# print(f"Принятые аргументы: {sys.argv}")
# print("Заканчиваю работать")
#
#
#
#
#
#
# from abc import ABC, abstractmethod
#
# # Класс оргтехники
# class Orgtechnik(ABC):
#     def __init__(self, name, company, count, sales=False, in_stock=False):
#         self.name = name
#         self.company = company
#         self.count = count
#         self.sales = sales
#         self.in_stock = in_stock
#
#     # Абстрактный метод проверки товара на продажу
#     @abstractmethod
#     def check_sales(self):
#         pass
#
#     @abstractmethod
#     def to_warehouse(self):
#         pass
#
#     # Перемещение на склад
#     def to_warehouse(self):
#         if self.in_stock == False:
#             if self.count > 0:
#                 self.in_stock = True
#                 res = f'Внимание! Товар {self.name} перемещен на склад в количестве {self.count} шт.'
#             else:
#                 res = f'Внимание! Товар {self.name} закончился. Перемещение невозможно.'
#         else:
#             res = f'Внимание! Товар {self.name} уже на складе в количестве {self.count} шт.'
#         print(res)
#
#     # Продажи товара
#     def sale(self):
#         if self.count == 0:
#             res = f'Внимание! Весь товар {self.name} продан'
#             self.sale = True
#
#         else:
#             self.count = self.count - 1
#             res =  f"Товар {self.name} продан в количестве 1 шт. Остаток {self.count}"
#         print(res)
#
#
#
#
#
# @check_password
# class Printer(Orgtechnik):
#
#     def __init__(self, name, type, company, count, in_stock, comment):
#         super().__init__(name, company, count, in_stock)
#         self.type = type
#         self.comment = comment
#
#     def check_sales(self):
#         if self.sales == 0:
#             res = 'Нет в наличии'
#         else:
#             res = 'Есть в наличии'
#         return res
#
#     def __str__(self):
#         res = Printer.check_sales(self)
#         res_text = f'''\nОписание принтера
# ----------------------------------------------
# Название: {self.name}
# Тип: {self.type}
# Компания: {self.company}
# Количество: {self.count}
# Статус: {res}
# Коментар: {self.comment}
# ----------------------------------------------
#         '''
#         return  res_text
#
#     def add_comment(self, new_comment):
#         self.comment = self.comment + '; ' + new_comment
#         return self.comment
#
#     def req_cartridge_repl(self):
#         pass

from logging import  getLogger, StreamHandler

logger = getLogger(__name__)

# DEBUG
# INFO
# WARNING
# ERROR

class MyTestClass():

    def __init__(self, name):
        self.name = name
        time.sleep(2)

a = MyTestClass("Nykodiuk")

