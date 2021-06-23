





import sqlite3
import json
import datetime
from flask import Flask
from datetime import datetime

conn = sqlite3.connect("order_service_db.db")
cursor = conn.cursor()

my_apply = Flask("my_first_app")

@my_apply.route('/ping')
def ping():
    return f"OK {datetime.now()}"

@my_apply.route("/check_method", methods=["GET", "POST", "UPDATE", "DELETE", "PUT"])
def checking():
    return f"OK {datetime.now()}"

my_apply.run()


# Класс подразделений
insert_data_log = '''INSERT INTO log(created_dt, type, comment) VALUES(?,?,?);'''
insert_data_dep = '''INSERT INTO departments(department_name) VALUES(?);'''
update_data_dep = '''UPDATE departments SET department_name = ? WHERE department_id = ?;'''
delete_data_dep = '''DELETE FROM departments WHERE department_id = ?;'''

# Создание логов
@staticmethod
def create_log(p_type, p_comment):
    with conn:
        cursor.execute(insert_data_log, (datetime.now(), p_type, p_comment))

    # Проверка наличия департамента в БД
@staticmethod
def check_dep(p_dep_name):
    check_dep = conn.cursor()
    sql_check = f'''select department_id from departments where department_name = "{p_dep_name}" limit 1;'''
    check_dep.execute(sql_check)
    res = check_dep.fetchone()

    return  res

    # Создание нового департамента
@my_apply.route('/create_app/<string:dep_name>', method=["GET","POST"])
def create_dep(dep_name):
    res = check_dep(dep_name)

    if res is None:
        cr_dep = conn.cursor()
        cr_dep.execute(insert_data_dep, (dep_name,))
        conn.commit()
        cr_dep.close()

        res_text = f"Добавлен департамент с параметрами dep_name:{dep_name}"
        print(res_text)

        # Добавление лога
        create_log("create_dep",res_text)
    else:
        print(f"Ошибка. Департамент с таким именем уже существует. Его id: {res[0]}")

    return "OK"

# Плохой вариант обновления, по имени департамента.
def update_dep_by_name(self, p_new_name_dep, p_department_id):
    res = Departments.__check_dep(self.dep_name)
    if res is None:
        print(f"Ошибка. Департамента с таким именем не существует.")
    else:
        with conn:

            upd_dep = conn.cursor()
            upd_dep.execute(Departments.__update_data_dep, (p_new_name_dep, p_department_id,))
            conn.commit()
            upd_dep.close()

            #cursor.execute(Departments.__update_data_dep, (p_new_name_dep, p_department_id))

            res_text = f"Обновлён департамент id:{p_department_id}, новое название dep_name: `{p_new_name_dep}`"
            print(res_text)

        Departments.create_log("update_dep_by_name", res_text)

@staticmethod
def delete_dep_by_id(p_department_id):
    del_dep = conn.cursor()
    del_dep.execute(delete_data_dep, (p_department_id,))
    conn.commit()
    del_dep.close()
    #with conn:
    #    cursor.execute(Departments.__delete_data_dep, p_department_id)
    res_text = f"Удалён департамент с id: {p_department_id}"
    print(res_text)

    create_log("delete_dep_by_name", res_text)

@staticmethod
def get_all_dep():
    check_apply = conn.cursor()
    sql_check = 'select department_id, department_name from departments'
    check_apply.execute(sql_check)
    res = check_apply.fetchall()

    print("\n          ДЕПАРТАМЕНТЫ          ")
    for i in res:
        res_text = f"""
--------------------------------
ID: {i[0]}
Название: {i[1]}
--------------------------------
"""
        print(res_text)

def __str__(self):
    res_txt = f'''Обычный вывод.
Департамент: {self.dep_name}
'''
    return res_txt

def __repr__(self):
    res_txt = f'''Машинный вывод. 
Департамент: {self.dep_name}
'''
    return res_txt

# Запись json кода в файл по id департамента
@staticmethod
def get_json(p_dep_id):
    try:

        check_dep = conn.cursor()
        sql_check = f'''
        select "department_id", "department_name"
        UNION ALL
        select department_id, department_name 
        from departments 
        where department_id = {p_dep_id};'''
        check_dep.execute(sql_check)
        res = check_dep.fetchall()

        a = res[0]
        b = res[1]
        res_new = json.loads(json.dumps(list(zip(a, b))))
        c = dict(res_new)

        with open(f"{p_dep_id}_dep.json", "w", encoding="UTF-8") as json_f:
            json.dump(c, json_f, ensure_ascii=False)
    except Exception:
        print(f"Ошибка! Департамент с таким ID не найдено")
#
# # Класс заявки
# class Apply(Departments):
#
#     __insert_data_appl = """INSERT INTO applications(created_dt, order_type, description, status, serial_no, creator_id) VALUES($1, $2, $3, $4, $5, $6)"""
#     __update_st_appl = """UPDATE applications SET status = $1, updated_dt = $2 WHERE order_id = $3"""
#     __update_desc_appl = """UPDATE applications SET description = $1, updated_dt = $2 WHERE order_id = $3"""
#     __update_creator_appl = """UPDATE applications SET creator_id = $1, updated_dt = $2 WHERE order_id = $3"""
#     __delete_data_appl = """DELETE FROM applications WHERE order_id = $1"""
#
#     def __init__(self, order_type, description, status, serial_no, creator_id):
#         self.status = "New"
#         self.order_type = order_type
#         self.description = description
#         self.status = status
#         self.serial_no = serial_no
#         self.creator_id = creator_id
#
#     def __str__(self):
#         res_text = f'''\nОбычный вывод. Заявка
# Тип: {self.order_type}
# Описание: {self.description}
# Статус: {self.status}
# SN: {self.serial_no}
# ID автора: {self.creator_id}
# '''
#         return res_text
#
#     def __repr__(self):
#         res_text = f'''\nМашинный вывод. Заявка
# Тип: {self.order_type}
# Описание: {self.description}
# Статус: {self.status}
# SN: {self.serial_no}
# ID автора: {self.creator_id}
# '''
#         return res_text
#
#     # проверка наличия сотрудника в БД, который создаёт заявку
#     def _check_emp(self, p_creator_id):
#         try:
#             check_creators = conn.cursor()
#             sql_check = f""" select employee_id from employees where employee_id = {p_creator_id} limit 1;"""
#             check_creators.execute(sql_check)
#             res = check_creators.fetchone()
#             return res
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     def __check_apply(self, p_order_id):
#         try:
#             check_apply = conn.cursor()
#             sql_check = f""" select order_id from applications where order_id = {p_order_id} limit 1;"""
#             check_apply.execute(sql_check)
#             res = check_apply.fetchone()
#             return res
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     # Создание заявки по serial_num
#     def create_apply(self):
#         try:
#             res = Apply._check_emp(self, self.creator_id)
#             if res is None:
#                 print(f"Ошибка. Не найден сотрудник с вказаным id: {self.creator_id}")
#             else:
#                 with conn:
#                     cursor.execute(Apply.__insert_data_appl, (datetime.now(),self.order_type, self.description, self.status, self.serial_no, self.creator_id))
#                 res_text = f"Добавлена запись с параметрами order_type:`{self.order_type}`, description:`{self.description}`, serial_no:{self.serial_no}, creator_id:{self.creator_id}"
#                 print(res_text)
#
#                 # добавление лога с помощью метода из наследованого класса Departments
#                 Departments.create_log(self, "create_apply",res_text)
#
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     # Обновление статуса заявки по order_id
#     def change_status_apply(self, p_new_status, p_order_id):
#         try:
#             with conn:
#                 cursor.execute(Apply.__update_st_appl, (p_new_status, datetime.now(), p_order_id))
#
#             res_text = f"Изменен статус по заявке order_id:{p_order_id} на `{p_new_status}`"
#             print(res_text)
#
#             # добавление лога с помощью метода из наследованого класса Departments
#             Departments.create_log(self, "change_status_apply", res_text)
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     # Обновление описания заявки по order_id
#     def change_description_apply(self, p_new_descr, p_order_id):
#         try:
#             with conn:
#                 cursor.execute(Apply.__update_desc_appl, (p_new_descr, datetime.now(), p_order_id))
#
#             res_text = f"Изменено описание по заявке order_id:{p_order_id} на `{p_new_descr}`"
#             print(res_text)
#
#             # добавление лога с помощью метода из наследованого класса Departments
#             Departments.create_log(self, "change_description_apply", res_text)
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     # Обновление id создателя по order_id
#     def change_creator_apply(self, p_order_id, p_new_creator_id):
#         try:
#             res = Apply._check_emp(self, p_new_creator_id)
#
#             # Если не найден сотрудник с таким id, выведем текст ошибки
#             if res is None:
#                 print(f"Ошибка. Не найден сотрудник с вказаным id: {p_new_creator_id}")
#             # Если всё хорошо, обновим
#             else:
#                 with conn:
#                     cursor.execute(Apply.__update_creator_appl, (p_new_creator_id, datetime.now(), p_order_id))
#
#                 res_text = f"Изменен creator_id по заявке order_id:{p_order_id} на `{p_new_creator_id}`"
#                 print(res_text)
#
#                 # добавление лога с помощью метода из наследованого класса Departments
#                 Departments.create_log(self, "change_creator_apply", res_text)
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     # Удаление заявки
#     def delete_apply(self, p_order_id):
#         try:
#             with conn:
#                 cursor.execute(Apply.__delete_data_appl, p_order_id)
#
#             res_text = f"Удалена заявка с id:{p_order_id}"
#             print(res_text)
#
#             # добавление лога с помощью метода из наследованого класса Departments
#             Departments.create_log(self, "delete_apply", res_text)
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     # Получение данных о заявке
#     def get_info_apply(self, p_order_id):
#         try:
#             res = Apply.__check_apply(self, p_order_id)
#
#             if res is None:
#                 res_text = f"Ошибка. Заявку з order_id: {p_order_id} не найдено."
#
#             else:
#                 check_apply = conn.cursor()
#                 sql_check = f""" select a.order_id, a.created_dt, a.order_type, a.description, a.status, a.serial_no, e.fio
#                                 from applications a
#                                 join employees    e ON a.creator_id = e.employee_id
#                                 where order_id = {p_order_id};"""
#                 check_apply.execute(sql_check)
#                 res = check_apply.fetchone()
#
#                 res_text = f'''\n               Информация по заявке
#     ----------------------------------------------------
#     ID: {res[0]}
#     Дата создания: {res[1]}
#     Тип: {res[2]}
#     Описание: {res[3]}
#     Статус: {4}
#     SN: {5}
#     Автор: {6}
#     ----------------------------------------------------
#     '''
#
#             return res_text
#
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     # Запись json кода в файл по id заявки
#     @staticmethod
#     def get_json(id_apply):
#         try:
#             check_apply = conn.cursor()
#             sql_check = f"""
#                           select 'order_id', 'created_dt', 'order_type', 'description', 'status', 'serial_no'
#                           union all
#                           select a.order_id, a.created_dt, a.order_type, a.description, a.status, a.serial_no
#                           from applications a
#                           where a.order_id = {id_apply};"""
#             check_apply.execute(sql_check)
#             res = check_apply.fetchall()
#             a = res[0]
#             b = res[1]
#             res_new = json.loads(json.dumps(list(zip(a, b))))
#             c = dict(res_new)
#
#             with open(f"{id_apply}_app.json", "w", encoding="UTF-8") as json_f:
#                 json.dump(c, json_f,ensure_ascii=False)
#         except Exception:
#             print(f"Ошибка! Заявку с таким ID не найдено")
#
# # Класс сотрудников
# class Employees(Departments):
#
#     __insert_data_emp = '''INSERT INTO employees(fio, position, department_id)  VALUES(?, ?, ?)'''
#     __update_fio_emp = '''UPDATE employees SET fio = ? WHERE employee_id = ?;'''
#     __update_pos_emp = '''UPDATE employees SET position = ? WHERE employee_id = ?;'''
#     __update_dep_emp = '''UPDATE employees SET department_id = ? WHERE employee_id = ?;'''
#     __delete_emp = '''DELETE FROM employees WHERE employee_id = ?;'''
#     __get_info_emp = '''SELECT e.employee_id, e.fio, e.position, d.department_name FROM employees e JOIN departments d ON e.department_id = d.department_id WHERE employee_id = ?'''
#
#     def __init__(self, fio, position, department_id):
#         self.fio = fio
#         self.position = position
#         self.department_id = department_id
#
#     def __str__(self):
#         res_txt = f'''Обычный вывод. Информация о сотруднике
# ---------------------------------------------
# ФИО: {self.fio}
# Должность: {self.position}
# ---------------------------------------------
# '''
#         return res_txt
#
#     def __repr__(self):
#         res_txt = f'''Машинный вывод. Информация о сотруднике
# ---------------------------------------------
# ФИО: {self.fio}
# Должность: {self.position}
# ---------------------------------------------
# '''
#         return res_txt
#
#     @staticmethod
#     def __check_emp(p_fio, p_departmnet_id):
#         try:
#             check_emp = conn.cursor()
#             sql_check = f'''select employee_id from employees where fio like '%{p_fio}%' and department_id = {p_departmnet_id} limit 1;'''
#             check_emp.execute(sql_check)
#             res = check_emp.fetchone()
#             return res
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     def create_emp(self):
#         try:
#
#             res = Employees.__check_emp(self.fio, self.department_id)
#
#             if res is None:
#
#                 inst_emp = conn.cursor()
#                 inst_emp.execute(Employees.__insert_data_emp,(self.fio, self.position, self.department_id,))
#                 conn.commit()
#                 inst_emp.close()
#
#                 res_text = f"Добавлен сотрудник с параметрами fio:{self.fio}, position:{self.position}" \
#                            f", department_id:{self.department_id}"
#                 print(res_text)
#
#                 # добавление лога с помощью метода наследованого из класа Departments
#                 Departments.create_log("create_emp", res_text)
#             else:
#                 print(f"Ошибка создания. Сотрудник с такими параметрами уже существует с id: {res[0]}")
#
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     @staticmethod
#     def update_fio_emp(p_new_fio, p_emp_id):
#         try:
#             res = Employees.__check_emp(p_new_fio, p_emp_id)
#             if res is None:
#                 print("Не найден сотрудник с такими данными")
#
#             else:
#
#                 upd_fio_emp = conn.cursor()
#                 upd_fio_emp.execute(Employees.__update_fio_emp,(p_new_fio, p_emp_id,))
#                 conn.commit()
#                 upd_fio_emp.close()
#
#                 res_text = f"Изменено ФИО по сотруднику с id:{p_emp_id} на `{p_new_fio}`"
#                 print(res_text)
#
#                 # добавление лога с помощью метода из наследованого класса Departments
#                 Departments.create_log("update_fio_emp", res_text)
#
#         except Exception as err:
#             print(f"Ошибка. {err}")
#
#     @staticmethod
#     def update_pos_emp(p_new_pos, p_emp_id):
#
#         upd_pos_emp = conn.cursor()
#         upd_pos_emp.execute(Employees.__update_pos_emp,(p_new_pos, p_emp_id,))
#         conn.commit()
#         upd_pos_emp.close()
#
#         res_text = f"Изменено должность по сотруднику с id:{p_emp_id} на `{p_new_pos}`"
#         print(res_text)
#
#         # добавление лога с помощью метода из наследованого класса Departments
#         Departments.create_log("update_pos_emp", res_text)
#
#     @staticmethod
#     def update_dep_emp(p_new_dep, p_emp_id):
#
#         upd_dep_emp = conn.cursor()
#         upd_dep_emp.execute(Employees.__update_dep_emp, (p_new_dep, p_emp_id,))
#         conn.commit()
#         upd_dep_emp.close()
#
#         res_text = f"Изменено отдел по сотруднику с id:{p_emp_id} на `{p_new_dep}`"
#         print(res_text)
#
#         # добавление лога с помощью метода из наследованого класса Departments
#         Departments.create_log("update_dep_emp", res_text)
#
#     @staticmethod
#     def delete_emp(p_emp_id):
#         del_emp = conn.cursor()
#         del_emp.execute(Employees.__delete_emp, (p_emp_id,))
#         conn.commit()
#         del_emp.close()
#
#         res_text = f"Удалён сотрудник с id:{p_emp_id}"
#         print(res_text)
#
#         # добавление лога с помощью метода из наследованого класса Departments
#         Departments.create_log("delete_emp", res_text)
#
#     @staticmethod
#     def get_info_emp(p_emp_id):
#         get_emp = conn.cursor()
#         get_emp.execute(Employees.__get_info_emp, (p_emp_id,))
#         res = get_emp.fetchone()
#         res_text =f'''\n        Информация о сотруднике id:{res[0]}
# --------------------------------------------
# "ФИО": {res[1]}
# "Должность": {res[2]}
# "Отдел": {res[3]}
# --------------------------------------------
#         '''
#
#         print(res_text)
#
#         # Запись json кода в файл по id (pk) департамент
#
#     @staticmethod
#     def get_json(id_emp):
#         try:
#
#             check_emp = conn.cursor()
#             sql_check = f'''
#             select "employee_id", "fio", "position", "department_id"
#             UNION ALL
#             select employee_id, fio, position, department_id
#             from employees
#             where employee_id = {id_emp};'''
#             check_emp.execute(sql_check)
#             res = check_emp.fetchall()
#
#             a = res[0]
#             b = res[1]
#             res_new = json.loads(json.dumps(list(zip(a, b))))
#             c = dict(res_new)
#
#             with open(f"{id_emp}_emp.json", "w", encoding="UTF-8") as json_f:
#                 json.dump(c, json_f, ensure_ascii=False)
#         except Exception:
#             print(f"Ошибка! Сотрудника с таким ФИО или ID не найдено")
#
#
# # ЗАЯВКИ
# print("ЗАЯВКИ: ")
#
# # 1) Создание заявки
# #apl1 = Apply("PDL",	"Продукт New_tax_45_pdl_10, период: 7d", "Sold", 312652, 1)
# #apl1.create_apply()
#
# # 2) Изменение статуса заявки по order_id
# #Apply.change_status_apply(apl1,"New",1)
#
# # 3) Изменение описания заявки по order_id
# #Apply.change_description_apply(apl1,"New descr",1)
#
# # 4) Изменение создателя заявки
# #Apply.change_creator_apply(apl1,'2',6)
#
# # 5) Удаление заявки по order_id
# #Apply.delete_apply(apl1,'1')
#
# # 6) Получение информации о заявк
# #print(Apply.get_info_apply(1,1))
#
# # 7) Запись информации о заявке в json
# Apply.get_json(1)
#
#
#
#
# # Депратаменты
# print("ДЕПАРТАМЕНТЫ: ")
#
# # 1) Создание департамента
# #dep1 = Departments("Ит")
# #Departments.create_dep(dep1)
#
# # 2) Изменение имени департамента по id
# #Departments.update_dep_by_name(dep1,"IT",1)
#
# # 3) Удаление департамента по id
# #Departments.delete_dep_by_id(12)
#
# # 6) Получение списка департаментов и их id
# #Departments.get_all_dep()
#
# # 7) Запись информации о департаменте в json
# Departments.get_json(2)
#
#
# # Сотрудники
# print("СОТРУДНИКИ: ")
#
# # 1) Создание сотрудника
# #emp1 = Employees('Никодюк Дмитрий Витальевич', 'Аналитик БД', 19)
# #emp1.create_emp()
#
# # 2) Изменение фио сотрудника
# #Employees.update_fio_emp("Никодюк Дмитрий Витальевич1",19)
#
# #    Изменение должности сотрудника
# #Employees.update_pos_emp("Тестировшик",1)
#
# #    Изменение отдела сотрудника
# #Employees.update_dep_emp(3,1)
#
# # 3) Удаление сотрудника из БД
# #Employees.delete_emp(21)
#
# # 4) Получение информации о сотруднике
# #Employees.get_info_emp(1)
#
# # 5) Запись информации о сотруднике в json
# Employees.get_json(1)

conn.close()