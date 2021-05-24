import sqlite3

my_empl = [("Никодюк Дмитрий Витальевич","Аналитик БД", 1)
    , ("Гусь Оксана Викторовна", "Руководитель отдела кадров", 3)
    , ("Голенков Виктор Генадьевич", "Начальник службы безопасности", 4)
    , ("Галупа Наталья Ивановна", "Специалист отдела кадров", 3)
    , ("Николаенко Ольга Васильевна", "Специалист отдела продаж", 2)
    , ("Бойко Елена Владимировна", "Специалист отдела продаж", 2)]

depart = [("Ит")
    , ("Продажи")
    , ("Отдел кадров")
    , ("СБ")]

appl = [("PDL", "Продукт New_tax_45_pdl_10, период: 7d", "Sold", 312651, 5)
    , ("PDL", "Продукт Act_tax_12_pdl_30, период: 14d", "Active", 157246, 6)
    , ("INST", "Продукт Max_tax_35_inst_5, период: 1m", "Closed", 721314, 6)
    , ("PDL", "Продукт Private_tax_15_pdl_10, период: 24d", "New", 236213, 5)
    , ("INST", "Продукт New_tax_20_inst_40, период: 2w", "Active", 634134, 6)
    , ("INST", "Продукт VIP_tax_10_inst_10, период: 1w", "Active", 910742, 5)
    , ("PDL", "Продукт Max_tax_40_inst_50, период: 6m", "Active", 725273, 5)]

conn = sqlite3.connect("order_service_db.db")
create_appl = conn.cursor()
# applications , таблица заявок
appl_sql = """CREATE TABLE IF NOT EXISTS applications  (
    order_id    INTEGER      PRIMARY KEY AUTOINCREMENT,
    created_dt DATETIME DEFAULT CURRENT_TIMESTAMP, -- автоматическая подстановка даты создания заявки во время добавления записи в таблицу
    updated_dt  DATETIME DEFAULT CURRENT_TIMESTAMP, -- автоматическая подстановка даты обновления заявки во время добавления записи в таблицу
    order_type  VARCHAR (50),
    description TEXT,
    status      VARCHAR (50),
    serial_no   INTEGER,
    creator_id  INTEGER      REFERENCES employees (employee_id) ON DELETE CASCADE
                                                                ON UPDATE SET NULL
);
"""
# Создан тригер для автоматического обновления поля updated_dt при обновлении данных в таблице
appl_triger_sql = """CREATE TRIGGER IF NOT EXISTS update_time
        BEFORE UPDATE
            ON applications
      FOR EACH ROW
          WHEN NEW.updated_dt <= old.updated_dt
BEGIN
    UPDATE applications
       SET updated_dt = CURRENT_TIMESTAMP
     WHERE order_id = old.order_id;
END;
"""

create_appl.execute(appl_sql)
create_appl.execute(appl_triger_sql)
create_appl.close()


create_empl = conn.cursor()
# employees , таблица сотрудников
empl_sql = """CREATE TABLE IF NOT EXISTS employees (
    employee_id   INTEGER       PRIMARY KEY AUTOINCREMENT,
    fio           VARCHAR (150),
    position      VARCHAR (150),
    department_id INTEGER       REFERENCES departments (department_id) ON DELETE CASCADE
                                                                       ON UPDATE SET NULL
);
"""
create_empl.execute(empl_sql)
create_empl.close()


create_dep = conn.cursor()
# departmenrs , таблица подразделений
create_dep_sql = """CREATE TABLE IF NOT EXISTS departments (
    department_id   INTEGER       PRIMARY KEY AUTOINCREMENT,
    department_name VARCHAR (255)
);
"""
create_dep.execute(create_dep_sql)
create_dep.close()


cursor = conn.cursor()
# -- insert-ы для вставки данных из кортежей
insert_data_dep = """INSERT INTO departments(department_name)
VALUES($1)
"""

insert_data_empl = """INSERT INTO employees(fio, position, department_id) 
VALUES($1, $2, $3)
"""

insert_data_appl = """INSERT INTO applications(order_type, description, status, serial_no, creator_id) 
VALUES($1, $2, $3, $4, $5)
"""

# -- Заполнение таблиц данными из кортежей
with conn:
    for row_dep in depart:
        print(f"Добавлено в таблицу departments: {row_dep}")
        cursor.execute(insert_data_dep, [row_dep])


with conn:
    for row_emp in my_empl:
        print(f"Добавлено в таблицу employeers: {row_emp}")
        cursor.execute(insert_data_empl, row_emp)

with conn:
    for row_appl in appl:
        print(f"Добавлено в таблицу applications: {row_appl}")
        cursor.execute(insert_data_appl, row_appl)

cursor.close()

def get_apl_on_date(in_dt):
    print(f"\nЗаявки за {in_dt}\n")
    sel_apl = conn.cursor()
    sql = f"""SELECT *
    FROM applications a
    WHERE date(a.created_dt) = '{in_dt}'
    """
    sel_apl.execute(sql)

    for row in sel_apl:
        print(row)

def get_apl_by_creator_fio(emp_fio):
    print(f"\nЗаявки по сотруднику {emp_fio}%\n")
    sel_apl = conn.cursor()
    sql = f"""SELECT e.fio, a.*
FROM applications a
join employees    e ON a.creator_id = e.employee_id
WHERE e.fio like '%{emp_fio}%'
    """
    sel_apl.execute(sql)

    for row in sel_apl:
        print(row)

def get_empl_departments():
    print("\nСотрудники и департаменты, в каких они работают\n")
    sel_empl = conn.cursor()
    sql = """SELECT e.employee_id, e.fio, e.position, d.department_name
FROM employees        e 
LEFT JOIN departments d ON e.department_id = d.department_id
;
    """
    sel_empl.execute(sql)
    for row in sel_empl:
        print(row)

def get_apl_by_date_and_status(dt1, dt2, status):
    print(f"\nЗаявки за промежуток времени с {dt1} - {dt2} в статусе {status}\n")
    sel_apl = conn.cursor()
    sql = f"""SELECT date(a.created_dt) as dt_created, count(1) as count_apl
FROM applications a
WHERE a.status = '{status}'
  and date(a.created_dt) between '{dt1}' and '{dt2}'
GROUP BY date(created_dt)
;
    """
    sel_apl.execute(sql)
    for row in sel_apl:
        print(row)

# Получение заявок за определенную дату
get_apl_on_date('2021-05-23')

# Получение заявок по сотруднику, работает через like '%name%'
get_apl_by_creator_fio('Бой')

# Вывод списка сотрудников и департаментов, в которых они работают
get_empl_departments()

# Вывод количества заявок по статусу за промежуток времени
get_apl_by_date_and_status('2021-05-20','2021-05-24','Active')








