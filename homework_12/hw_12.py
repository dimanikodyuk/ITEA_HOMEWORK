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
import json
from flask import Flask, request

conn = sqlite3.connect("../order_service_db.db", check_same_thread=False)
my_apply = Flask("my_first_app")

# Список сотрудников в обработку
list_emp = []
# Результатирующий список
finish_list = []

def thread_function(name, p_emp_id):
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
       "%s: %s, %s: %s" % (name, p_emp_id, c, dates)
    )

# Ручка для передачи пользователем id сотрудников на обработку
@my_apply.route("/check_emp", methods=["POST"])
def get_emp():

    emp_id_list = request.json.get('emp_list', None)
    threads = list()
    k = 0
    for index in emp_id_list:
        x = Thread(target=thread_function, args=(index, emp_id_list[k]))
        threads.append(x)
        x.start()
        x.join()
        k = k+1

    return {
        "status": 1,
        "result": finish_list
        #"result": f"Успешно начат поиск по сотрудникам с номерами: {list_emp}"
    }

my_apply.run(debug=True)