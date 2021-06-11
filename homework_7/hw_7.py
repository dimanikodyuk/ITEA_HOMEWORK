import sqlite3
import datetime
import time
from datetime import datetime

conn = sqlite3.connect("order_service_db.db")
cursor = conn.cursor()


# Класс подразделений
class Departments():

    __date_now = datetime.now()
    __insert_data_log = """INSERT INTO log(created_dt, type, comment) VALUES($1, $2, $3) """
    __insert_data_dep = """INSERT INTO departments(department_name) VALUES($1) """
    __update_data_dep = """UPDATE departments SET department_name = $1 WHERE department_id = $2; """
    __delete_data_dep = """DELETE FROM departments WHERE department_id = "$1" """

    def __init__(self, dep_name):
        self.dep_name = dep_name

    # Создание логов
    def create_log(self, p_type, p_comment):
        with conn:
            cursor.execute(Departments.__insert_data_log, (Departments.__date_now, p_type, p_comment))

    # Проверка наличия департамента в БД
    def __check_dep(self):

        check_dep = conn.cursor()
        sql_check = f'''select department_id from departments where department_name = $1 limit 1;''',(self.dep_name)
        check_dep.execute(sql_check)
        res = check_dep.fetchone()

        return  res[0]

    # Создание нового департамента
    def create_dep(self):
        res = Departments.__check_dep(self.dep_name)

        if res is None:
            with conn:
                cursor.execute(Departments.__insert_data_dep, (self.dep_name))

            res_text = f"Добавлен департамент с параметрами dep_name:{self.dep_name}"
            print(res_text)

            # Добавление лога
            Departments.create_log(self,"create_dep",res_text)
        else:
            print(f"Ошибка. Департамент с таким именем уже существует. Его id: {res[0]}")

    # Плохой вариант обновления, по имени департамента.
    def update_dep_by_name(self, p_new_name_dep, p_department_id):
        res = Departments.__check_dep(self.dep_name)
        if res is None:
            print(f"Ошибка. Департамента с таким именем не существует.")
        else:
            with conn:
                cursor.execute(Departments.__update_data_dep, (p_new_name_dep, p_department_id))

                res_text = f"Обновлён департамент id:{p_department_id}, новое название dep_name: `{p_new_name_dep}`"
                print(res_text)

            Departments.create_log(self, "update_dep_by_name", res_text)

    def delete_dep_by_name(self, p_department_id):
        res = Departments.__check_dep(self.dep_name)

        if res is None:
            print(f"Ошибка. Департамента с таким именем не существует.")
        else:
            with conn:
                cursor.execute(Departments.__delete_data_dep, (p_department_id))

            res_text = f"Удалён департамент с названием:`{p_department_id}`"
            print(res_text)

            Departments.create_log(self, "delete_dep_by_name", res_text)

    def __str__(self):
        return self.dep_name

# Класс заявки
class Apply(Departments):

    __insert_data_appl = """INSERT INTO applications(created_dt, order_type, description, status, serial_no, creator_id) VALUES($1, $2, $3, $4, $5, $6)"""
    __update_st_appl = """UPDATE applications SET status = $1, updated_dt = $2 WHERE order_id = $3"""
    __update_desc_appl = """UPDATE applications SET description = $1, updated_dt = $2 WHERE order_id = $3"""
    __update_creator_appl = """UPDATE applications SET creator_id = $1, updated_dt = $2 WHERE order_id = $3"""
    __delete_data_appl = """DELETE FROM applications WHERE order_id = $1"""
    def __init__(self, order_type, description, status, serial_no, creator_id):
        self.status = "New"
        self.order_type = order_type
        self.description = description
        self.status = status
        self.serial_no = serial_no
        self.creator_id = creator_id

    def __str__(self):
        res_text = f'''
        Тип: {self.order_type}
        Описание: {self.description}
        Статус: {self.status}
        SN: {self.serial_no}
        ID автора: {self.creator_id}
        '''

    # проверка наличия сотрудника в БД, который создаёт заявку
    def _check_emp(self, p_creator_id):
        check_creators = conn.cursor()
        sql_check = f""" select employee_id from employees where employee_id = {p_creator_id} limit 1;"""
        check_creators.execute(sql_check)
        res = check_creators.fetchone()
        return res

    def __check_apply(self, p_order_id):
        check_apply = conn.cursor()
        sql_check = f""" select order_id from applications where order_id = {p_order_id} limit 1;"""
        check_apply.execute(sql_check)
        res = check_apply.fetchone()
        return res

    # Создание заявки по serial_num
    def create_apply(self):
        res = Apply._check_emp(self, self.creator_id)
        if res is None:
            print(f"Ошибка. Не найден сотрудник с вказаным id: {self.creator_id}")
        else:
            with conn:
                cursor.execute(Apply.__insert_data_appl, (datetime.now(),self.order_type, self.description, self.__status, self.serial_no, self.creator_id))
            res_text = f"Добавлена запись с параметрами order_type:`{self.order_type}`, description:`{self.description}`, serial_no:{self.serial_no}, creator_id:{self.creator_id}"
            print(res_text)

            # добавление лога с помощью метода из наследованого класса Departments
            Departments.create_log(self, "create_apply",res_text)

    # Обновление статуса заявки по order_id
    def change_status_apply(self, p_new_status, p_order_id):
        with conn:
            cursor.execute(Apply.__update_st_appl, (p_new_status, datetime.now(), p_order_id))

        res_text = f"Изменен статус по заявке order_id:{p_order_id} на `{p_new_status}`"
        print(res_text)

        # добавление лога с помощью метода из наследованого класса Departments
        Departments.create_log(self, "change_status_apply", res_text)

    # Обновление описания заявки по order_id
    def change_description_apply(self, p_new_descr, p_order_id):
        with conn:
            cursor.execute(Apply.__update_desc_appl, (p_new_descr, datetime.now(), p_order_id))

        res_text = f"Изменено описание по заявке order_id:{p_order_id} на `{p_new_descr}`"
        print(res_text)

        # добавление лога с помощью метода из наследованого класса Departments
        Departments.create_log(self, "change_description_apply", res_text)

    # Обновление id создателя по order_id
    def change_creator_apply(self, p_order_id, p_new_creator_id):

        res = Apply._check_emp(self, p_new_creator_id)

        # Если не найден сотрудник с таким id, выведем текст ошибки
        if res is None:
            print(f"Ошибка. Не найден сотрудник с вказаным id: {p_new_creator_id}")
        # Если всё хорошо, обновим
        else:
            with conn:
                cursor.execute(Apply.__update_creator_appl, (p_new_creator_id, datetime.now(), p_order_id))

            res_text = f"Изменен creator_id по заявке order_id:{p_order_id} на `{p_new_creator_id}`"
            print(res_text)

            # добавление лога с помощью метода из наследованого класса Departments
            Departments.create_log(self, "change_creator_apply", res_text)

    # Удаление заявки
    def delete_apply(self, p_order_id):
        with conn:
            cursor.execute(Apply.__delete_data_appl, p_order_id)

        res_text = f"Удалена заявка с id:{p_order_id}"
        print(res_text)

        # добавление лога с помощью метода из наследованого класса Departments
        Departments.create_log(self, "delete_apply", res_text)

    # Получение данных о заявке
    def get_info_apply(self, p_order_id):
        res = Apply.__check_apply(self, p_order_id)

        if res is None:
            res_text = f"Ошибка. Заявку з order_id: {p_order_id} не найдено."

        else:
            check_apply = conn.cursor()
            sql_check = f""" select a.order_id, a.created_dt, a.order_type, a.description, a.status, a.serial_no, e.fio
                            from applications a
                            join employees    e ON a.creator_id = e.employee_id
                            where order_id = {p_order_id};"""
            check_apply.execute(sql_check)
            res = check_apply.fetchone()

            res_text = f'''\n               Информация по заявке 
----------------------------------------------------
ID: {res[0]}
Дата создания: {res[1]}
Тип: {res[2]}
Описание: {res[3]}
Статус: {4}
SN: {5}
Автор: {6}
----------------------------------------------------
'''

        return res_text

# Класс сотрудников
class Employees(Departments):

    __insert_data_emp = """INSERT INTO employees(fio, position, department_id)  VALUES($1, $2, $3)"""

    def __init__(self, fio, position, department_id):
        self.fio = fio
        self.position = position
        self.department_id = department_id

    def __check_emp(self):
        check_emp = conn.cursor()
        sql_check = f'''select employee_id from employees where fio like '%{self.fio}%' and department_id = {self.department_id} limit 1;'''
        check_emp.execute(sql_check)
        res = check_emp.fetchone()
        return res[0]


    def create_emp(self):
        res = Employees.__check_emp(self)

        if res is None:
            with conn:
                cursor.execute(Employees.__insert_data_emp, (self.fio, self.position, self.department_id))

            res_text = f"Добавлен сотрудник с параметрами fio:{self.fio}, position:{self.position}, department_id:{self.department_id}"
            print(res_text)

            # добавление лога с помощью метода наследованого из класа Departments
            Departments.create_log(self, "create_emp", res_text)
        else:
            print(f"Ошибка. Сотрудник с такими параметрами уже существует с id: {res[0]}")


    def update_fio_emp(self):
        res = Employees.__check_emp()

# ЗАЯВКИ
print("ЗАЯВКИ: ")

# 1) Создание заявки
apl1 = Apply("PDL",	"Продукт New_tax_45_pdl_10, период: 7d", "Sold", 312652, 5)
apl1.create_apply()

# 2) Изменение статуса заявки по order_id
Apply.change_status_apply(apl1,"New",1)

# 3) Изменение описания заявки по order_id
Apply.change_description_apply(apl1,"New descr",1)

# 4) Изменение создателя заявки
Apply.change_creator_apply(apl1,'2',6)

# 5) Удаление заявки по order_id
Apply.delete_apply(apl1,'1')

# 6) Получение информации о заявк
print(Apply.get_info_apply(1,30))



#dep1 = Departments("Ит")
#dep1.create_dep()

#emp1 = Employees("Никодюк Дмитрий Витальевич1", "Аналитик БД", 1)
#emp1.create_emp()


conn.close()