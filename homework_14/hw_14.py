import sqlite3
import json
import datetime
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#conn = sqlite3.connect("order_service_db.db", check_same_thread=False)

DB_URL = "sqlite:///order_service_db.db"

my_apply = Flask("my_first_app")
my_apply.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(my_apply)

class Departments(db.Model):
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100))

class Employees(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fio = db.Column(db.String(100), unique=True)
    position = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))

class Applications(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_dt = db.Column(db.DateTime)
    updated_dt = db.Column(db.DateTime)
    order_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    serial_no = db.Column(db.Integer, unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_dt = db.Column(db.DateTime)
    type = db.Column(db.String(100))
    comment = db.Column(db.Text)


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

# Проверка наличия департамента в БД
def check_dep_name(p_dep_name):
    # запрос в БД
    sql_dep = db.select(Departments.department_id).where(Departments.department_name == f'{p_dep_name}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

def check_dep_id(p_dep_id):
    # запрос в БД
    sql_dep = db.select(Departments.department_id).where(Departments.department_id == f'{p_dep_id}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

# Создание нового департамента
@my_apply.route("/create_dep", methods=["POST"])
def create_dep():

    if request.method == "POST":
        dep_data = json.loads(request.data)
        dep_name = dep_data["department_name"]

        res = check_dep_name(dep_name)

        if res is None:
            dep_cr = Departments(department_name=dep_name)
            db.session.add(dep_cr)
            db.session.flush()

            dt = datetime.now()
            log_text = f"Добавлен департамент с параметрами dep_name:{dep_name}"
            log = Log(created_dt=dt, type="create_apl", comment=log_text)
            db.session.add(log)
            db.session.flush()

            db.session.commit()

            return render_template("change_department.html", dep_data=dep_data)
        else:
            return render_template("change_department.html", dep_data={"ОШИБКА: Департамент уже существует"})

# Обновление департамента по id
@my_apply.route("/update_dep", methods=["POST"])
def update_dep_by_name():
    if request.method == "POST":
        dep_data = json.loads(request.data)
        dep_name_old = dep_data["department_name_old"]
        dep_name_new = dep_data["department_name_new"]

        res = check_dep_name(dep_name_old)
        if res is None:
            return render_template("departments.html", dep_data="ОШИБКА: Департамент не существует")
        else:

            # запрос в БД
            dep = Departments.query.get(res[0])
            dep.department_name = dep_name_new
            db.session.commit()

            #sql_dep = db.update(Departments).where(Departments.department_id == f'{res[0]}').values(Departments.department_name == f'{dep_name_new}')
            #print(sql_dep)

            dt = datetime.now()
            log_text = f"Обновлён департамент с id {res[0]}."
            log = Log(created_dt=dt, type="update_dep", comment=log_text)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            return render_template("departments.html", dep_data=f"ИНФО: Обновлено департамент id {res[0]}. Новое имя {dep_name_new}")

@my_apply.route("/delete_dep/<int:dep_id>", methods=["DELETE"])
def delete_dep_by_id(dep_id):
    if request.method == "DELETE":
        res = check_dep_id(dep_id)
        if res is None:
            return render_template("change_department.html", dep_data=f"ОШИБКА: Подразделения с таким id не существует")
        else:
            dep = Departments.query.get(res[0])
            db.session.delete(dep)
            db.session.commit()
            return render_template("change_department.html", dep_data=f"ИНФО: Удалён департамент с id {dep_id}")

@my_apply.route("/get_all_dep", methods=["GET", "POST"])
def get_all_dep():
    if request.method == 'POST':
        cou_row = request.form.get('cou_row')
        if cou_row == "0":
            rec = db.session.query(Departments).all()
        else:
            rec = db.session.query(Departments).limit(cou_row).all()
        res_arr_a = []
        for i in rec:
            res_arr_a.append((i.__dict__['department_id'], i.__dict__['department_name']))
        return render_template("departments.html", dep_list=res_arr_a)
    else:
        return render_template("departments.html", dep_list="")

def check_emp(p_fio):
    # запрос в БД
    sql_dep = db.select(Employees.employee_id).where(Employees.fio == f'{p_fio}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

def check_emp_id(p_emp_id):
    # запрос в БД
    sql_dep = db.select(Employees.employee_id).where(Employees.employee_id == f'{p_emp_id}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

@my_apply.route("/create_emp", methods=["POST"])
def create_emp():
    if request.method == "POST":
        emp_data = json.loads(request.data)

        fio = emp_data['fio']
        position = emp_data['position']
        dep_id = emp_data['dep_id']

        res = check_emp(fio)

        if res is None:

            emp_cr = Employees(fio=fio, position=position, department_id=dep_id)
            db.session.add(emp_cr)
            db.session.flush()

            dt = datetime.now()
            log_text = f"Добавлен сотрудник с параметрами fio:{fio}, position {position}, dep_id {dep_id}"
            log = Log(created_dt=dt, type="create_emp", comment=log_text)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            return render_template("employees.html", emp_result="ИНФО: Добавлен новый сотрудник")
        else:
            return render_template("employees.html", emp_result="ОШИБКА: Сотрудника не добавлено")

@my_apply.route("/update_emp", methods=["POST"])
def update_emp():
    if request.method == "POST":
        emp_data = json.loads(request.data)
        new_fio = emp_data["new_fio"]
        new_position = emp_data["new_position"]
        new_dep_id = emp_data["new_dep_id"]
        emp_id = emp_data["emp_id"]

        res = check_emp_id(emp_id)
        if res is None:
            return render_template("employees.html", emp_result="ОШИБКА: Сотрудник не найден")
        else:

            # запрос в БД
            emp = Employees.query.get(res[0])

            emp.fio = new_fio
            emp.position = new_position
            emp.department_id = new_dep_id

            db.session.commit()

            dt = datetime.now()
            log_text = f"Обновлён сотрудник с id {emp_id}, новые параметры fio:{new_fio}, position {new_position}, dep_id {new_dep_id}"
            log = Log(created_dt=dt, type="update_emp", comment=log_text)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            return render_template("employees.html", emp_result=f"ИНФО: Обновлено сотрудник id {emp_id}. Новое имя {new_fio}, должность: {new_position}, департамент: {new_dep_id}")

@my_apply.route("/delete_emp/<int:emp_id>", methods=["DELETE"])
def delete_emp(emp_id):
    if request.method == "DELETE":
        res = check_emp_id(emp_id)
        if res is None:
            return render_template("change_employees.html", emp_result=f"ОШИБКА: Сотрудника с таким id не существует")
        else:
            emp = Employees.query.get(res[0])
            db.session.delete(emp)
            db.session.commit()

            dt = datetime.now()
            log_text = f"Удалён сотрудник с id {emp_id}."
            log = Log(created_dt=dt, type="delete_emp", comment=log_text)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            return render_template("change_employees.html", emp_result=f"ИНФО: Удалён сотрудник с id {emp_id}")

@my_apply.route("/get_all_emp", methods=["GET", "POST"])
def get_all_emp():
    if request.method == 'POST':
        cou_row = request.form.get('cou_row')
        if cou_row == "0":
            rec = db.session.query(Employees).all()
        else:
            rec = db.session.query(Employees).limit(cou_row).all()
        res_arr_a = []
        for i in rec:
            res_arr_a.append((i.__dict__['employee_id'], i.__dict__['fio'], i.__dict__['position'], i.__dict__['department_id']))
        return render_template("employees.html", employees_list=res_arr_a)
    else:
        return render_template("employees.html", employees_list="")

#    { % if employees_lis | length > 1 %}



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

# проверка наличия сотрудника в БД, который создаёт заявку
def check_emp(p_creator_id):
    # запрос в БД
    sql_dep = db.select(Employees.employee_id).where(Employees.employee_id == f'{p_creator_id}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

def check_apply(p_app_id):
    # запрос в БД
    sql_dep = db.select(Applications.order_id).where(Applications.order_id == f'{p_app_id}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

@my_apply.route("/create_apply", methods=["POST"])
def create_apply():
    if request.method == "POST":
        emp_data = json.loads(request.data)
        order_type = emp_data['order_type']
        description = emp_data['description']
        serial_no = emp_data['serial_no']
        creator_id = emp_data['creator_id']
        status = "New"

        res = check_emp(creator_id)

        if res is None:
            return render_template("applications.html", apply_info="ОШИБКА: Не найдено указанного пользователя, кто создаёт заявку")
        else:
            dt = datetime.now()
            app_cr = Applications(created_dt=dt, order_type=order_type, description=description, status=status, serial_no = serial_no, creator_id =creator_id)
            db.session.add(app_cr)
            db.session.flush()

            dt = datetime.now()
            log_text = f"Создана заявка с параметрами created_dt:{dt}, order_type {order_type}, description {description}, serial_no {serial_no}, creator_id {creator_id}"
            log = Log(created_dt=dt, type="create_apply", comment=log_text)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            return render_template("applications.html", apply_info="ИНФО: Создана заявка")

# Обновление статуса заявки по order_id
@my_apply.route("/update_apply", methods=["POST"])
def change_apply():

    if request.method == "POST":
        apply_data = json.loads(request.data)
        order_type = apply_data["order_type"]
        description = apply_data["description"]
        serial_no = apply_data["serial_no"]
        creator_id = apply_data["creator_id"]
        status = apply_data["status"]
        apply_id = apply_data["apply_id"]

        res = check_apply(apply_id)
        if res is None:
            return render_template("applications.html", apply_info="ОШИБКА: Завку не найдено")
        else:

            dt = datetime.now()
            # запрос в БД
            apply = Applications.query.get(res[0])
            apply.updated_dt = dt
            apply.order_type = order_type
            apply.description = description
            apply.serial_no = serial_no
            apply.creator_id = creator_id
            apply.status = status

            db.session.commit()


            log_text = f"""Обновлена заявка с id {apply_id}, новые параметры order_type:{order_type}, description {description}, serial_no {serial_no}
            , creator_id {creator_id}, status {status}"""
            log = Log(created_dt=dt, type="update_apply", comment=log_text)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            return render_template("applications.html", apply_info=f"ИНФО: Обновлена заявка с id {apply_id}")

# Удаление заявки
@my_apply.route("/delete_apply/<int:apply_id>", methods=["DELETE"])
def delete_apply(apply_id):

    if request.method == "DELETE":
        res = check_apply(apply_id)
        if res is None:
            return render_template("applications.html", apply_info=f"ОШИБКА: Зявку с таким id не найдено")
        else:
            app = Applications.query.get(res[0])
            db.session.delete(app)
            db.session.commit()

            dt = datetime.now()
            log_text = f"Удалена заявка с id {apply_id}."
            log = Log(created_dt=dt, type="delete_apply", comment=log_text)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            return render_template("applications.html", apply_info=f"ИНФО: Удалена заявка с id {apply_id}")





@my_apply.route("/get_all_app", methods=["GET", "POST"])
def get_all_app():
    if request.method == 'POST':
        cou_row = request.form.get('cou_row')
        if cou_row == "0":
            rec = db.session.query(Applications).all()
        else:
            rec = db.session.query(Applications).limit(cou_row).all()
        res_arr_a = []
        for i in rec:
            res_arr_a.append((i.__dict__['order_id'], i.__dict__['created_dt'], i.__dict__['order_type'], i.__dict__['description'], i.__dict__['status'], i.__dict__['serial_no']))
        return render_template("applications.html", app_list=res_arr_a)
    else:
        return render_template("departments.html", dep_list="")



my_apply.run(debug=True)