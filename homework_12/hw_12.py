# from time import sleep
# import time
# import os
#
# #pid = os.getpid() # Получение ид процесса
#
# # создает точную копию родительского процесса
# pid = os.fork()
#
# if pid == 0: # id дочернего процесса всегда будет 0
#     # код будет исполнен в дочернем процессе
#     while True:
#         print("child:", os.getpid())
#         time.sleep(2)
#
# else:
#     # код будет исполнен в родительском процессе
#     print("parent:", os.getpid())
#     os.wait() # дожидаемся завершения всех дочерних процессов

#
# from multiprocessing import Process
# from time import sleep
# num_list = [x for x in range(10)]
#
# class MyShinyProcess(Process):
#
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#
#     def run(self):
#         try:
#             global num_list
#             proc_num = num_list.pop()
#             print("hello", self.name, proc_num)
#             sleep(1)
#             if len(num_list) != 0:
#                 p = MyShinyProcess("Mike")
#                 p.start()
#                 p.join()
#             print("%d FINISHED" % proc_num)
#         except Exception as err:
#             print(f"ERROR: {err}")
#
# p = MyShinyProcess("Mike")
# p.start()
# p.join()

# from concurrent.futures import ThreadPoolExecutor, as_completed
# from random import randrange
# from time import sleep
#
# b = 0
#
# def f(a):
#     global b
#     print("This is %d" %b)
#     b+=1
#     sleep_time = 1
#     sleep(sleep_time)
#     buf = b
#     return f"result {a * a} for thread {buf} which slept {sleep_time}"
#
# with ThreadPoolExecutor(max_workers=50) as pool:
#     results = [pool.submit(f, i) for i in range(10)]
#
#     for future in as_completed(results):
#         print(future.result())



from threading import Thread
from datetime import datetime
import sqlite3
import requests
import json
from flask import Flask, request

conn = sqlite3.connect("order_service_db.db", check_same_thread=False)
my_apply = Flask("my_first_app")

class myThread (Thread):
   def __init__(self, name, emp_id):
       Thread.__init__(self)
       self.name = name
       self.emp_id = emp_id

   def run(self):
       print("Starting " + self.name)
       return_json_emp(self.name, self.emp_id)
       print("Exiting " + self.name)

# Список сотрудников в обработку
list_emp = []
# Результатирующий список
finish_list = []


# Ручка для передачи пользователем id сотрудников на обработку
@my_apply.route("/check_emp", methods=["POST"])
def get_emp():

    emp_id_list = request.json.get('emp_list', None)
    list_emp = list(map(str, emp_id_list.split()))

    return {
        "status": 1,
        "result": finish_list
        #"result": f"Успешно начат поиск по сотрудникам с номерами: {list_emp}"
    }


def return_json_emp(threadName, p_emp_id):
    get_emp = conn.cursor()
    get_sql = f"""SELECT 'employee_id', 'fio', 'position', 'department_id' UNION ALL
    SELECT employee_id, fio, position, department_id  from employees where employee_id = {p_emp_id}"""
    get_emp.execute(get_sql)
    dates = datetime.now()
    res = get_emp.fetchall()
    a = res[0]
    b = res[1]
    res_new = json.loads(json.dumps(list(zip(a, b))))
    c = dict(res_new)
    finish_list.append(c)
    get_emp.close()
    print(
       "%s: %s, %s: %s" % ( threadName, p_emp_id, c, dates)
    )

    return finish_list

#
# # Создать треды
# thread1 = myThread("Thread", 1)
# thread2 = myThread("Thread", 2)
# thread3 = myThread("Thread", 3)
# # Запустить треды
# thread1.start()
# thread2.start()
# thread3.start()
#
# thread1.join()
# thread2.join()
# thread3.join()



my_apply.run(debug=True)