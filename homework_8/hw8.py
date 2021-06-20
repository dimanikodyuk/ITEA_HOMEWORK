# ЗАДАНИЕ №1
from datetime import datetime
#
# def time_cheker(my_obj):
#     def timer_func(*args, **kwargs):
#         res = my_obj(*args, **kwargs)
#         res_addr = hex(id(res)) # адрес памяти экземпляра класса
#         f = open("add_object_class.txt", "a", encoding="UTF-8")
#         current_datetime = datetime.now()
#         f.writelines(f'{current_datetime.strftime("%d-%m-%Y %H:%M")} Создан экземпляр класса {my_obj.__name__} по адресу памяти {res_addr} \n')
#         f.close()
#         return res
#
#     return timer_func
#
#
# @time_cheker
# class Departments:
#
#     def __init__(self, dep_name):
#         self.dep_name = dep_name
#
#     def __str__(self):
#         return self.dep_name
#
# dep = Departments("Test1")
# dep2 = Departments("Test2")
# dep3 = Departments("Test3")
# print(dep)
# print(dep2)
# print(dep3)

# Задание №2
# 2. На основе прошлых ДЗ необходимо создать модели представлений для классов ДЕПАРТАМЕНТЫ (Departments),
# СОТРУДНИКИ (Employees), ЗАЯВКИ (Orders). Реализовать магические методы вывода информации на экран как для пользователя,
# так и для "машинного" отображения.
#
#
# Предусмотреть все необходимые ограничения и связи моделей между собой.
#
#
# У каждой модели предусмотрите метод, который бы мог осуществлять запись хранимой в экземпляре информации в отдельный
# json-файл с именем вида <id записи>.json. Если id не существует - выдавать ошибку.



# import json
#
# products = {
#     'Onion': {
#         'price': 12,
#         'in_stock': 1000,
#         'description': 'Лук'
#     },
#     'Tomato': {
#         'price': 4,
#         'in_stock': 10000,
#         'description': 'Помидоры'
#     },
#     'Cucumber': {
#         'price': 10,
#         'in_stock': 500,
#         'description': 'Огурцы',
#         # 'test' : {1, 2, 3}
#     }
# }
#
# json_object = json.dumps(products)
# print(json_object)
# print(type(json_object))
#
# with open("products_data.json", "w", encoding="UTF-8") as json_f:
#     json.dump(products, json_f)

# ЗАДАНИЕ №2
import mongoengine as me
import json
me.connect("LESSON_9")

departments = []
employees = []

# Класс подразделений
class Departments(me.Document):

    dep_name = me.StringField(required=True, min_length=2)

    def __str__(self):
        res = f'''Обычный вывод информации о департаменте {self.pk}
---------------------------------------------------
Департамент: {self.dep_name}
---------------------------------------------------
'''
        return res

    def __repr__(self):
        res = f'''Машинный вывод информации о департаменте {self.pk}
---------------------------------------------------
Департамент: {self.dep_name}
---------------------------------------------------
'''
        return res

    # Запись json кода в файл по id (pk) департамент
    @staticmethod
    def get_json(id_dep):
        try:
            res = Departments.objects.get(pk=id_dep)
            res_json = json.loads(res.to_json())
            with open(f"{id_dep}.json", "w", encoding="UTF-8") as json_f:
                json.dump(res_json, json_f)
        except Exception:
            print(f"Ошибка! Департамент с таким ID не найдено")


# Класс сотрудников
class Employees(me.Document):

    fio = me.StringField(required=True, min_length=10)
    position = me.StringField(required=True, min_length=10)
    department_id = me.IntField(Departments, required=True)

    def __str__(self):
       res = f'''\nОбычный вывод информации о сотруднике {self.pk}
----------------------------------------------------
ФИО: {self.fio}
Долженость: {self.position}
Департамент: {self.department_id}
----------------------------------------------------
'''
       return res

    def __repr__(self):
        res = f'''\nМашинный вывод информации о сотруднике {self.pk}
----------------------------------------------------
ФИО: {self.fio}
Долженость: {self.position}
Департамент: {self.department_id}
----------------------------------------------------
        '''
        return res

    # Запись json кода в файл по id (pk) сотрудника
    @staticmethod
    def get_json(id_emp):
        try:
            res = Departments.objects.get(pk=id_emp)
            res_json = json.loads(res.to_json())
            with open(f"{id_emp}.json", "w", encoding="UTF-8") as json_f:
                json.dump(res_json, json_f)
        except Exception:
            print(f"Ошибка! Сотрудника с таким ID не найдено")

    # @staticmethod
    # def __check_emp(p_fio, p_departmnet_id):
    #     try:
    #         check_emp = conn.cursor()
    #         sql_check = f'''select employee_id from employees where fio like '%{p_fio}%' and department_id = {p_departmnet_id} limit 1;'''
    #         check_emp.execute(sql_check)
    #         res = check_emp.fetchone()
    #         return res
    #     except Exception as err:
    #         print(f"Ошибка. {err}")
    #
    # def create_emp(self):
    #     try:
    #
    #         res = Employees.__check_emp(self.fio, self.department_id)
    #
    #         if res is None:
    #
    #             inst_emp = conn.cursor()
    #             inst_emp.execute(Employees.__insert_data_emp,(self.fio, self.position, self.department_id,))
    #             conn.commit()
    #             inst_emp.close()
    #
    #             res_text = f"Добавлен сотрудник с параметрами fio:{self.fio}, position:{self.position}" \
    #                        f", department_id:{self.department_id}"
    #             print(res_text)
    #
    #             # добавление лога с помощью метода наследованого из класа Departments
    #             Departments.create_log("create_emp", res_text)
    #         else:
    #             print(f"Ошибка создания. Сотрудник с такими параметрами уже существует с id: {res[0]}")
    #
    #     except Exception as err:
    #         print(f"Ошибка. {err}")



    #
    # @staticmethod
    # def delete_emp(p_emp_id):
    #     del_emp = conn.cursor()
    #     del_emp.execute(Employees.__delete_emp, (p_emp_id,))
    #     conn.commit()
    #     del_emp.close()
    #
    #     res_text = f"Удалён сотрудник с id:{p_emp_id}"
    #     print(res_text)
    #
    #     # добавление лога с помощью метода из наследованого класса Departments
    #     Departments.create_log("delete_emp", res_text)

# Класс заявок
class Apply(me.Document):
    order_type = me.StringField(required=True, min_length=2)
    desc = me.StringField(required=True, min_length=10, max_length=100)
    status = me.StringField(default="New")
    serial_no = me.IntField(required=True)
    creator_id = me.IntField() # me.StringField(Employees, required=True) #, reverse_delete_ryle=me.CASCADE)

    def __str__(self):
        res = f'''\nОбычный вывод информации по заявке {self.pk}:
----------------------------------------------------
Тип: {self.order_type}
Описание: {self.desc}
Статус: {self.status}
Серийный №: {self.serial_no}
Создатель: {self.creator_id}
---------------------------------------------------- 
'''
        return res

    def __repr__(self):
        res = f'''\nМашинный вывод информации по заявке {self.pk}:
----------------------------------------------------
Тип: {self.order_type}
Описание: {self.desc}
Статус: {self.status}
Серийный №: {self.serial_no}
Создатель: {self.creator_id}
---------------------------------------------------- 
        '''
        return res

    # Запись json кода в файл по id (pk) заявки
    @staticmethod
    def get_json(id_apply):
        try:
            res = Apply.objects.get(pk=id_apply)
            res_json = json.loads(res.to_json())
            with open(f"{id_apply}.json", "w", encoding="UTF-8") as json_f:
                json.dump(res_json, json_f)
        except Exception:
            print(f"Ошибка! Заявку с таким ID не найдено")


#res = Apply.objects.get(status="New")
#
# dep1 = Departments(dep_name="911")
# dep1.save()

Apply.get_json('60cf66b1e2f4bfaefa4143c5')


# res = Departments.objects.all()
# k = 0
# for item in res:
#
#     #js_data = item.to_json()
#     dict_data = json.loads(item.to_json())
#     departments.append({"id": dict_data['_id']['$oid'], "value": dict_data['dep_name']})
#     k = k + 1
#
# print(departments)



# dep1 = Departments.objects(pk='60cf711db5d629278eefb5c2')
# employer1 = Employees(fio="Никодюк Д.В.", position="Аналитик БД", department_id=dep1).save()
#


#empl = Employees.objects.get('')
#Apply.objects.get(desc="test").delete()
#print(res)

#first_apply = Apply(order_type='2w', desc="Minimal_tax10", serial_no=742541)
#first_apply.save()

# res = Apply.objects.all()
# for item in res:
#     print(item)
#     js_data = item.to_json()
#     print(js_data)
#     dict_data = json.loads(item.to_json())
#     print(dict_data)


