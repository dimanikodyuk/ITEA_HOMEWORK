import sqlite3
import json
import datetime
from flask import Flask, request, render_template, Response
from datetime import datetime

conn = sqlite3.connect("order_service_db.db", check_same_thread=False)

my_apply = Flask("my_first_app")

@my_apply.route('/ping')
def ping():
    return {
        "status": 1,
        "result": f"PING SUCCESSFUL {datetime.now()}"
    }


@my_apply.route('/', methods=["GET", "POST"])
@my_apply.route('/main', methods=["GET", "POST"])
def homepage():
    return render_template("index.html")


@my_apply.route("/check_method", methods=["GET", "POST", "UPDATE", "DELETE", "PUT"])
def checking():
    return f"OK {datetime.now()}"

# Создание логов
def create_log(p_type, p_comment):
    cr_log = conn.cursor()
    sql_log = f"""INSERT INTO log(created_dt, type, comment) VALUES('{datetime.now()}','{p_type}','{p_comment}');"""
    cr_log.execute(sql_log)
    cr_log.close()

# Проверка наличия департамента в БД
def check_dep_name(p_dep_name):
    ch_dep = conn.cursor()
    sql_check = f'''select department_id from departments where department_name = "{p_dep_name}" limit 1;'''
    ch_dep.execute(sql_check)
    res = ch_dep.fetchone()
    ch_dep.close()

    return res

def check_dep_id(p_dep_id):
    ch_dep = conn.cursor()
    sql_check = f'''select department_id from departments where department_id = "{p_dep_id}" limit 1;'''
    ch_dep.execute(sql_check)
    res = ch_dep.fetchone()
    ch_dep.close()

    return res

# Создание нового департамента
@my_apply.route("/create_dep/<string:dep_name>", methods=["POST"])
def create_dep(dep_name):
    res = check_dep_name(dep_name)

    if res is None:
        cr_dep = conn.cursor()
        cr_sql = f"""INSERT INTO departments(department_name) VALUES('{dep_name}');"""
        cr_dep.execute(cr_sql)
        conn.commit()
        cr_dep.close()

        log_text = f"Добавлен департамент с параметрами dep_name:{dep_name}"
        res_text = {
            "status": 1,
            "result": log_text
        }

        # Добавление лога
        create_log("create_dep", log_text)
        return res_text
    else:
        res_text = {
            "status": 0,
            "result": f"Ошибка. Департамент с таким именем уже существует. Его id: {res[0]}"
        }
        return res_text

# Обновление департамента по id
@my_apply.route("/update_dep", methods=["POST"])
def update_dep_by_name():

    dep_old = request.json.get('dep_old', None)
    dep_new = request.json.get('dep_new', None)

    res = check_dep_name(dep_old)

    if res is None:
        res_text = {
            "status": 0,
            "result": "Ошибка. Департамента с таким именем не существует."
        }
        return res_text
    else:
        with conn:
            upd_dep = conn.cursor()
            upd_sql = f"""UPDATE departments SET department_name = '{dep_new}' WHERE department_name = '{dep_old}';"""
            upd_dep.execute((upd_sql))
            conn.commit()
            upd_dep.close()

        log_text = f"Обновлён департамент: {dep_old}, новое название dep_name: {dep_new}"
        res_text = {
            "status": 1,
            "result": log_text
        }
        create_log("update_dep_by_name", log_text)
        return res_text

@my_apply.route("/delete_dep/<int:dep_id>", methods=["DELETE"])
def delete_dep_by_id(dep_id):
    try:
        res = check_dep_id(dep_id)
        if res is None:
            return {
                "status": 0,
                "result": f"Не найден департамент с id: {dep_id}"
            }
        else:
            del_dep = conn.cursor()
            del_sql = f"""DELETE FROM departments WHERE department_id = {dep_id};"""
            del_dep.execute(del_sql)
            conn.commit()
            del_dep.close()

            res_log = f"Удалён департамент с id: {dep_id}"
            res_text = {
                "status": 1,
                "result": res_log
            }
            create_log("delete_dep_by_name", res_log)
            return res_text
    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка: {err}"
        }

@my_apply.route("/get_all_dep", methods=["GET", "POST"])
def get_all_dep():
    if request.method == 'POST':

        cou_row = request.form.get('cou_row')
        if cou_row == '0':
            get_dep = conn.cursor()
            dep_sql = f"""select department_id, department_name from departments;"""
            get_dep.execute(dep_sql)
            res = get_dep.fetchall()
            get_dep.close()
            return render_template("departments.html", dep_list=res)
        else:
            get_dep = conn.cursor()
            dep_sql = f"""select department_id, department_name from departments limit {cou_row};"""
            get_dep.execute(dep_sql)
            res = get_dep.fetchall()
            get_dep.close()
            return render_template("departments.html", dep_list=res)
    else:
        return render_template("departments.html", del_list="")

# Запись json кода в файл по id департамента
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
        return {
            "status": 0,
            "result": "Ошибка! Департамент с таким ID не найдено"
            }

def check_emp(p_fio, p_departmnet_id):
    try:
        check_emp = conn.cursor()
        sql_check = f'''select employee_id 
                        from employees 
                        where fio like '%{p_fio}%' and department_id = {p_departmnet_id} limit 1;'''
        check_emp.execute(sql_check)
        res = check_emp.fetchone()
        return res
    except Exception as err:
        return {"status": 0, "result": (f"Ошибка. {err}")}

@my_apply.route("/create_emp", methods=["POST"])
def create_emp():
    try:
        fio = request.json.get('fio', None)
        position = request.json.get('position', None)
        dep_id = request.json.get('dep_id', None)

        res = check_emp(fio, dep_id)

        if res is None:

            inst_emp = conn.cursor()
            inst_sql = f"""INSERT INTO employees(fio, position, department_id)  VALUES('{fio}', '{position}', {dep_id})"""
            inst_emp.execute(inst_sql)
            conn.commit()
            inst_emp.close()

            log_text = f"Добавлен сотрудник с параметрами fio:{fio}, position:{position}, department_id:{dep_id}"
            res_text = {
                "status": 1,
                "res_text": log_text
            }

            # добавление лога с помощью метода наследованого из класа Departments
            create_log("create_emp", log_text)

            return res_text
        else:
            res_text = {
                "status": 0,
                "res_text": f"Ошибка создания. Сотрудник с такими параметрами уже существует с id: {res[0]}"
            }
            return res_text

    except Exception as err:
        return {"status": 0, "result": f"Ошибка. {err}"}

@my_apply.route("/update_emp", methods=["POST"])
def update_emp():
    try:
        new_fio = request.json.get('new_fio', None)
        new_position = request.json.get('new_position', None)
        new_dep_id = request.json.get('new_dep_id', None)
        emp_id = request.json.get('emp_id', None)

        upd_emp = conn.cursor()
        upd_sql = f"""UPDATE employees 
                        SET fio = '{new_fio}', position = '{new_position}', department_id = {new_dep_id} 
                        WHERE employee_id = {emp_id};"""
        upd_emp.execute(upd_sql)
        conn.commit()
        upd_emp.close

        log_text = f"Изменено данные сотрудника, fio: {new_fio}, position: {new_position}, dep_id: {new_dep_id}"

        res_text = {
            "status": 1,
            "result": log_text
        }

        return  res_text

    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка {err}"
        }

@my_apply.route("/delete_emp/<int:emp_id>", methods=["DELETE"])
def delete_emp(emp_id):
    try:
        del_emp = conn.cursor()
        del_sql = f'DELETE FROM employees WHERE employee_id = {emp_id};'
        del_emp.execute(del_sql)
        conn.commit()
        del_emp.close()

        res_log = f"Удалён сотрудник с id:{emp_id}"
        res_text = {
            "status": 1,
            "result": res_log
        }

        # добавление лога с помощью метода из наследованого класса Departments
        create_log("delete_emp", res_log)
        return res_text

    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка: {err}"
        }

@my_apply.route("/get_all_emp", methods=["GET", "POST"])
def get_all_emp():
    if request.method == 'POST':
        cou_row = request.form.get('cou_row')
        if cou_row == '0':
            get_emp = conn.cursor()
            get_sql = f"""SELECT e.employee_id, e.fio, e.position, d.department_name 
                                FROM employees   e
                                JOIN departments d ON e.department_id = d.department_id
                """
            get_emp.execute(get_sql)
            res = get_emp.fetchall()
            get_emp.close()
            return render_template("employees.html", employees_list=res)
        else:
            get_emp = conn.cursor()
            get_sql = f"""SELECT e.employee_id, e.fio, e.position, d.department_name 
                                FROM employees   e
                                JOIN departments d ON e.department_id = d.department_id
                                LIMIT {cou_row}
                """
            get_emp.execute(get_sql)
            res = get_emp.fetchall()
            get_emp.close()
            return render_template("employees.html", employees_list=res)
    else:
        return render_template("employees.html", employees_list="")

@my_apply.route("/create_json_emp/<int:emp_id>", methods=["POST"])
def get_json_emp(emp_id):
    try:
        check_emp = conn.cursor()
        sql_check = f'''select "employee_id", "fio", "position", "department_id"
                        UNION ALL
                        select employee_id, fio, position, department_id
                        from employees
                        where employee_id = {emp_id};'''
        check_emp.execute(sql_check)
        res = check_emp.fetchall()

        a = res[0]
        b = res[1]
        res_new = json.loads(json.dumps(list(zip(a, b))))
        c = dict(res_new)

        with open(f"{emp_id}_emp.json", "w", encoding="UTF-8") as json_f:
            json.dump(c, json_f, ensure_ascii=False)

        return {
            "status": 1,
            "result": f"Успещно создан файл {emp_id}_emp.json"
        }
    except Exception:
        return {
            "status": 0,
            "result": f"Ошибка! Сотрудника с таким ФИО или ID не найдено"
        }



# проверка наличия сотрудника в БД, который создаёт заявку
def check_emp(p_creator_id):
    try:
        check_creators = conn.cursor()
        sql_check = f""" select employee_id from employees where employee_id = {p_creator_id} limit 1;"""
        check_creators.execute(sql_check)
        res = check_creators.fetchone()
        return res
    except Exception as err:
        print(f"Ошибка. {err}")

def check_apply(p_order_id):
    try:
        check_apply = conn.cursor()
        sql_check = f""" select order_id from applications where order_id = {p_order_id} limit 1;"""
        check_apply.execute(sql_check)
        res = check_apply.fetchone()
        return res
    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка. {err}"
        }

@my_apply.route("/create_apply", methods=["POST"])
def create_apply():
    try:
        order_type = request.json.get('order_type', None)
        description = request.json.get('description', None)
        serial_no = request.json.get('serial_no', None)
        creator_id = request.json.get('creator_id', None)
        status = "New"

        res = check_emp(creator_id)
        if res is None:
            return {
                "status": 0,
                "result": f"Ошибка. Не найден сотрудник с вказаным id: {creator_id}"
            }

        else:

            cr_app = conn.cursor()
            cr_sql = f"""INSERT INTO applications(created_dt, order_type, description, status, serial_no, creator_id) 
            VALUES('{datetime.now()}', '{order_type}', '{description}', '{status}', '{serial_no}', '{creator_id}')"""
            cr_app.execute(cr_sql)
            conn.commit()
            cr_app.close()

            res_log = f"Добавлена запись с параметрами order_type:{order_type}, description:{description}, serial_no:{serial_no}, creator_id:{creator_id}"
            res_text = {
                "status": 1,
                "result": res_log
            }

            # добавление лога с помощью метода из наследованого класса Departments
            create_log("create_apply",res_log)

            return res_text

    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка. {err}"
        }

# Обновление статуса заявки по order_id
@my_apply.route("/update_apply", methods=["POST"])
def change_apply():
    try:
        order_type = request.json.get('order_type', None)
        description = request.json.get('description', None)
        serial_no = request.json.get('serial_no', None)
        creator_id = request.json.get('creator_id', None)
        status = "New"
        apply_id = request.json.get('apply_id', None)

        res_a = check_apply(apply_id)
        res_b = check_emp(creator_id)

        if res_a is None:
            return {
                "status": 0,
                "result": f"Заявку с id {apply_id} не найдено."
            }
        elif res_b is None:
            return {
                "status": 0,
                "result": f"Сотрудника с id {creator_id} не найдено."
            }
        else:
            upd_app = conn.cursor()
            upd_sql = f"""UPDATE applications 
                            SET order_type='{order_type}', description='{description}', status='{status}'
                            , serial_no = {serial_no}, creator_id = {creator_id}
                            WHERE order_id = {apply_id}"""
            upd_app.execute(upd_sql)
            conn.commit()
            upd_app.close()

            res_log = f"""Измененны данные по заявке: order_type {order_type}, description {description}, status={status},
             serial_no={serial_no}, creator_id={creator_id}"""
            res_text = {
                "status": 1,
                "result": res_log
            }
            return res_text

        # добавление лога с помощью метода из наследованого класса Departments
        create_log(self, "change_status_apply", res_log)
    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка. {err}"
        }

# Удаление заявки
@my_apply.route("/delete_apply/<int:apply_id>", methods=["DELETE"])
def delete_apply(apply_id):
    try:
        res = check_apply(apply_id)
        if res is None:

            del_app = conn.cursor()
            del_sql = f"""DELETE FROM applications WHERE order_id = {apply_id}"""
            del_app.execute(del_sql)
            conn.commit()
            del_app.close()

            res_log = f"Удалена заявка с id:{apply_id}"
            res_text = {
                "status": 0,
                "result": res_log
            }

            # добавление лога с помощью метода из наследованого класса Departments
            create_log("delete_apply", res_log)

            return res_text
        else:
            return {
                "status": 0,
                "result": f"Заявку с id {apply_id} не найдено."
            }
    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка. {err}"
        }


# Получение данных о заявке
@my_apply.route("/apply_info/<int:apply_id>", methods=["GET"])
def get_info_apply(apply_id):
    try:

        check_apply = conn.cursor()
        sql_check = f""" select a.order_id, a.created_dt, a.order_type, a.description, a.status, a.serial_no, e.fio
                        from applications a
                        join employees    e ON a.creator_id = e.employee_id
                        where order_id = {apply_id};"""
        check_apply.execute(sql_check)
        res = check_apply.fetchone()

        return {
            "status": 1,
            "id": res[0],
            "created_dt": res[1],
            "order_type": res[2],
            "description": res[3],
            "status": res[4],
            "serial_no": res[5],
            "fio": res[6]
        }
    except Exception as err:
        return {
            "status": 0,
            "result": f"Ошибка: {err}"
        }

@my_apply.route("/get_all_app", methods=["GET", "POST"])
def get_all_app():

    if request.method == 'POST':

        cou_row = request.form.get('cou_row')
        if cou_row == '0' or None:
            get_app = conn.cursor()
            get_sql = f"""  SELECT a.order_id, a.created_dt, a.updated_dt, a.order_type, a.description, a.status, a.serial_no , e.fio
                                FROM applications a
                                JOIN employees    e ON a.creator_id    = e.employee_id
                   """
            get_app.execute(get_sql)
            res = get_app.fetchall()
            return render_template("applications.html", app_list=res)
        else:
            get_app = conn.cursor()
            get_sql = f"""  SELECT a.order_id, a.created_dt, a.updated_dt, a.order_type, a.description, a.status, a.serial_no , e.fio
                                FROM applications a
                                JOIN employees    e ON a.creator_id    = e.employee_id
                                LIMIT {cou_row}
                   """
            get_app.execute(get_sql)
            res = get_app.fetchall()
            return render_template("applications.html", app_list=res)
    else:
        return render_template("applications.html", app_list="")

# Запись json кода в файл по id заявки
@my_apply.route("/create_json_apply/<int:apply_id>", methods=["POST"])
def get_json_apply(apply_id):
    try:
        check_apply = conn.cursor()
        sql_check = f"""
                      select 'order_id', 'created_dt', 'order_type', 'description', 'status', 'serial_no'
                      union all
                      select a.order_id, a.created_dt, a.order_type, a.description, a.status, a.serial_no
                      from applications a
                      where a.order_id = {apply_id};"""
        check_apply.execute(sql_check)
        res = check_apply.fetchall()
        a = res[0]
        b = res[1]
        res_new = json.loads(json.dumps(list(zip(a, b))))
        c = dict(res_new)

        with open(f"{apply_id}_app.json", "w", encoding="UTF-8") as json_f:
            json.dump(c, json_f, ensure_ascii=False)
            return {
                "status": 1,
                "result": f"Создан файл: {apply_id}_app.json"
            }
    except Exception:
        return {
            "status": 0,
            "result": f"Ошибка! Заявку с таким ID не найдено"
        }


my_apply.run(debug=True)