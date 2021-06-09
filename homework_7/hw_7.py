import sqlite3
import datetime
import time
from datetime import datetime

conn = sqlite3.connect("order_service_db.db")
cursor = conn.cursor()


class Apply():

    def __init__(self, order_type, description, status, serial_no, creator_id):
        self.order_type = order_type
        self.description = description
        self.status = status
        self.serial_no = serial_no
        self.creator_id = creator_id

    # Создание заявки по serial_num
    def create_apply(self):
        insert_data_appl = """INSERT INTO applications(created_dt, order_type, description, status, serial_no, creator_id) 
        VALUES($1, $2, $3, $4, $5, $6)
        """

        with conn:
            cursor.execute(insert_data_appl, (datetime.now(),self.order_type, self.description, self.status, self.serial_no, self.creator_id))

    # Обновление статуса заявки по serial_num
    def change_status_apply(self, serial_num, new_status):
        update_st_appl = """
            UPDATE applications 
            SET status = $1
              , updated_dt = $2
            WHERE serial_no = $3
        """

        with conn:
            cursor.execute(update_st_appl, (new_status, datetime.now(), serial_num))

    # Обновление описания заявки по serial_num
    def change_description_apply(self, serial_num, new_descr):
        update_desc_appl = """
            UPDATE applications 
            SET description = $1
              , updated_dt = $2
            WHERE serial_no = $3
        """

        with conn:
            cursor.execute(update_desc_appl, (new_descr, datetime.now(), serial_num))

    # Обновление id создателя по serial_num
    def change_creator_apply(self, serial_num, new_creator_id):

        # Проверка есть ли такой сотрудник в БД, так как у нас есть соединение по PK - FK. В инном случае поломаем всё)
        check_creators = conn.cursor()
        sql_check = f""" select employee_id from employees where employee_id = {new_creator_id} limit 1;"""
        check_creators.execute(sql_check)
        res = check_creators.fetchone()

        # Если не найден сотрудник с таким id, выведем текст ошибки
        if res is None:
            print(f"Ошибка обновления ответственного по заявке. Не найден сотрудник с вказаным id: {new_creator_id}")
        # Если всё хорошо, обновим
        else:
            update_creator_appl = """
            UPDATE applications
            SET creator_id = $1
              , updated_dt = $2
            WHERE serial_no = $3
            """

            with conn:
                cursor.execute(update_creator_appl, (new_creator_id, datetime.now(), serial_num))

        check_creators.close()



class Departments():

    def __init__(self, dep_name):
        self.dep_name = dep_name

    # Создание нового департамента
    def create_dep(self):
        check_dep = conn.cursor()
        sql_check = f'''select department_id from departments where department_name = "{self.dep_name}" limit 1;'''
        check_dep.execute(sql_check)
        res = check_dep.fetchone()

        if res[0] is None:
            print("OK")
        else:
            print(f"Департамент с таким именем уже существует. Его id: {res[0]}")

    # Обновление департманета по ид
    def update_dep(self, dep_id, dep_name):
        update_dep = """
                    UPDATE departments 
                    SET department_name = $1
                    WHERE department_id = $2
                """
        with conn:
            cursor.execute(update_dep, (dep_name, dep_id))

class Employees():

    def __init__(self, fio, position, department_id):
        self.fio = fio
        self.position = position
        self.department_id = department_id

    def create_emp(self):
        check_emp = conn.cursor()
        sql_check = f'''select employee_id from employees where fio like '%{self.fio}%' and position like '%{self.position}%' 
        and department_id = {self.department_id} limit 1;
        '''

        check_emp.execute(sql_check)
        res = check_emp.fetchone()

        if res is None:

            insert_data_emp = """INSERT INTO employees(fio, position, department_id) 
                    VALUES($1, $2, $3)
                    """

            with conn:
                cursor.execute(insert_data_emp, (self.fio, self.position, self.department_id))

        else:
            print(f"Сотрудник с такими параметрами уже существует с id: {res[0]}")


#apl1 = Apply("PDL",	"Продукт New_tax_45_pdl_10, период: 7d", "Sold", 312654, 5)
#apl1.create_apply()

#time.sleep(2)

#Apply.change_creator_apply(1,312654,11)
#apl1.change_status_apply(312653,"Check2")
#apl1.change_description_apply(312653,"Тест")


dep1 = Departments("Ит")
dep1.create_dep()

emp1 = Employees("Никодюк Дмитрий Витальевич1", "Аналитик БД", 1)
emp1.create_emp()


conn.close()


