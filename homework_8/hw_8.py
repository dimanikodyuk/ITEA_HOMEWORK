import sys
import time
import sqlite3
from datetime import date
from logging import  getLogger, StreamHandler

#1 способ реализации Singletone
# class Connect:
#     cnt = 0
#     def __init__(self, dsn):
#         self.conn = sqlite3.connect(dsn)
#
#     def __new__(cls, *args, **kwargs):
#         if cls.cnt > 0:
#             raise Exception("Нельзя создавать больше одного экземпляра!")
#         cls.cnt += 1
#         return super().__new__(cls)

# 2 способ реализации Singletone
def singletone(cls):
    cnt = 0

    def inner(*args, **kwargs):
        nonlocal  cnt
        if cnt > 0:
            raise ValueError("Нельзя")
        cnt += 1
        return cls(*args, **kwargs)
    return inner

@singletone
class Connect:
    def __init__(self, dsn):
        self.conn = sqlite3.connect(dsn)

@singletone
class TestClass:
    pass


from datetime import datetime

# # !!! Нельзя наследоваться от класса, у которого есть декоратор !!! Нарушение принципов ООП.

my_conn = Connect("order_service_db.db")
#my_conn2 = Connect("order_service_db.db")
test_ex = TestClass()
test_ex1 = TestClass()

cursor = my_conn.conn.cursor()

secret_password = "1234"
#current_password = sys.argv[1] #введённый пароль
current_password = "1234"



logger = getLogger(__name__)

stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

# Декоратор
def check_password(f):
    def inner(*args, **kwargs):
        if secret_password == current_password:
            return f(*args, **kwargs)
        else:
            raise Exception("Wrong password!")
    return inner

def time_cheker(my_obj):
    def timer_func(*args, **kwargs):
        print("Начало выполнения.")
        st_time = time.time()
        time.sleep(1)
        my_obj(*args, **kwargs)
        end_time = ("%s second" % (time.time() - st_time))
        print("Конец выполнения.")
        print(f'Время выполнения {my_obj}: {end_time} \n')
    return timer_func


#
# print("Начинаю работать")
# # Получения аргументом из терминала с помощью команды sys.argv
# print(f"Принятые аргументы: {sys.argv}")
# print("Заканчиваю работать")
#

@time_cheker
class Departments():

    def __init__(self, dep_name):
        self.dep_name = dep_name



dep = Departments("Test")




# DEBUG
# INFO
# WARNING
# ERROR

logger.setLevel("DEBUG")
logger.debug("Сообщение уровня DEBUG")
logger.info("Сообщение уровня INFO")
logger.warning("Сообщение уровня WARNING")
logger.error("Сообщение уровня ERROR")





#
# class MyTestClass():
#
#     def __init__(self, name):
#         self.name = name
#         time.sleep(2)
#
# a = MyTestClass("Nykodiuk")

