# ЗАДАНИЕ №1
import mongoengine as me
import json
me.connect("LESSON_9")

# Проверка, чтобы переданный параметр был только с кирилических символов
def validator(s):
    for el in s:
        if not((1040 <= ord(el) <= 1103) or el in ["","_"," "]):
            raise me.ValidationError("Ошибка. Название должно состоять только из кирилических символов: %s" % (s, ))


# Класс подразделений
class Departments(me.Document):

    dep_name = me.StringField(validation=validator, required=True, min_length=2)

    # Создание департамента
    def create_dep(self):
        try:
            self.save()
            res_text = f'Департамент создан с id: {self.id}'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при создании департамента {self.id}:\n{err}'
        return res_text

    # Обновление департамента
    def update_dep(self, new_dep_name):
        try:
            self.dep_name = new_dep_name
            self.save()
            res_text = f'Обновлён департамент с id: {self.id}'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при обновлении данных департамента {self.id}:\n{err}'
        return res_text

    # Удаление департамента
    def delete_dep(self):
        try:
            self.delete()
            res_text = f'Департамент с id: {self.id} - успешно удалён'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при удалении департамента {self.id}:\n{err}'
        return res_text

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
    department_id = me.ReferenceField(Departments, required=True, reverse_delete_ryle=me.CASCADE)

    # Создание сотрудника
    def create_emp(self):
        try:
            self.save()
            res_text = f'Сотрудник создана с id: {self.id}'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при регистрации сотрудника {self.id}:\n{err}'
        return res_text

    # Обновление сотрудника
    def update_emp(self, new_fio, new_position):
        try:
            self.fio = new_fio
            self.position = new_position
            self.save()
            res_text = f'Обновлены данные сотрудника с id: {self.id}'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при обновлении данных сотрудника {self.id}:\n{err}'
        return res_text

    # Удаление сотрудника
    def delete_emp(self):
        try:
            self.delete()
            res_text = f'Сотрудник с id: {self.id} - успешно удалён'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при удалении записи сотрудника {self.id}:\n{err}'
        return res_text

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


# Класс заявок
class Apply(me.Document):
    order_type = me.StringField(required=True, min_length=2)
    desc = me.StringField(required=True, min_length=10, max_length=100)
    status = me.StringField(default="New")
    serial_no = me.IntField(required=True)
    creator_id = me.ReferenceField(Employees, required=True, reverse_delete_ryle=me.CASCADE)

    # Создание заявки
    def create_apply(self):
        try:
            self.save()
            res_text = f'Заявка создана с id: {self.id}'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при создании заявки {self.id}:\n{err}'
        return res_text

    # Обновление заявки
    def update_apply(self, new_order_type, new_desc, new_status, new_serial_no):
        try:
            self.order_type = new_order_type
            self.desc = new_desc
            self.status = new_status
            self.serial_no = new_serial_no
            self.save()

        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при обновлении заявки {self.id}:\n{err}'
        return res_text

    # Удаление заявки
    def delete_apply(self):
        try:
            self.delete()
            res_text = f'Заявка id: {self.id} - успешно удалена'
        except Exception as err:
            res_text = f'Внимание! Произошла ошибка при удалении заявки {self.id}:\n{err}'
        return  res_text

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


# Создание департамента
#print(Departments(dep_name="Певческий").create_dep())

# Обновление названия департамента
#dep1 = Departments.objects.get(id='60d1f4f79796c8edae0173a7')
#print(dep1.update_dep('911'))

# Удаление департамента
#print(dep1.delete_dep())




# Регистрация сотрудника
#get_dep = Departments.objects.get(id='60d1e11d4421a1ba88b99f18')
#print(Employees(fio="Совцова Лидия Олеговна",position="Аналитик БД",department_id=get_dep).create_emp())

# Обновление данных по сотруднику
#get_emp = Employees.objects.get(id='60d1e11d4421a1ba88b99f18')
#print(get_emp.update_emp('Омельченко Алексей Валерьевич','Поддержка рабочих мест'))

# Удаление сотрудника
#print(get_emp.delete_emp())



# Создание заявки
#get_emp = Employees.objects.get(fio="Никодюк Дмитрий Витальевич")
#print(Apply(order_type="2w",desc="1515asfdasda",serial_no=1516161,creator_id=get_emp).create_apply())

# Обновление данных по заявке
#apl1 = Apply.objects.get(id='60d1e56870a788910d585220')
#print(apl1.update_apply('7d','Test test tes 123','Test',9814981))

# Удаление заявки
#apl1.delete_apply()






