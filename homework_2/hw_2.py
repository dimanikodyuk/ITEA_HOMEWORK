# Задание №1
class Car():
    car_counter = 0

    def __init__(self, speed, color, name, is_police):
        Car.car_counter += 1
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

    def go(self):
        print(f"Машина {self.name} поехала")

    def stop(self):
        print(f"Машина {self.name} остановилась")

    def show_speed(self):
        return self.speed

    def turn(self, direction):
        if direction == "left":
            print(f"Поворот машины {self.name} налево")
        elif direction == "right":
            print(f"Поворот машины {self.name} направо")
        elif direction == "back":
            print(f"Машина {self.name} развернулась")
        else:
            print(f"Машина {self.name} укатилась в неизвестном направлении")

    def __str__(self):
        return f"""\nОписание автомобиля {self.name}:
-------------------------------------------------------------------------------------
Цвет: {self.color}.
Скорость: {self.show_speed()} км/ч.
-------------------------------------------------------------------------------------
"""

    @classmethod
    def show_car_counter(cls):
        return cls.car_counter


class TownCar(Car):
    max_town_car_speed = 60

    def show_speed(self):
        if self.speed > TownCar.max_town_car_speed:
            return f"Автомобить {self.name} превысил скорость в классе TownCar на {self.speed - self.max_town_car_speed} км/ч. Текущая скорость {self.speed}"
        else:
            return self.speed


class SportCar(Car):
    pass


class WorkCar(Car):
    max_work_car_speed = 40

    def show_speed(self):
        if self.speed > WorkCar.max_work_car_speed:
            print(f"Автомобить {self.name} превысил скорость в классе WorkCar на {self.speed - self.max_work_car_speed} км/ч. Текущая скорость {self.speed}")
        else:
            print(self.speed)


class PoliceCar(Car):
    pass


my_car1 = Car(120,"red","Ford",False)
my_car2 = TownCar(80, "white", "Renault", True)
my_car3 = SportCar(250, "black", "Suzuki", False)
my_car4 = WorkCar(41, "purple", "Honda", False)
my_car5 = PoliceCar(210, "white", "Lamborgini", True)

my_car3.go()
my_car3.turn("left")
my_car3.turn("back")
my_car3.stop()

print(my_car1)
print(my_car2)
print(my_car3)
print(my_car4)
print(my_car5)


# # Задание № 2
# import uuid
# import time
# from datetime import datetime
#
#
# class Application():
#
#     def __init__(self, first_name, serial_num, status):
#         self.__id = uuid.uuid4()
#         self.dt_create = datetime.now()
#         self.first_name = first_name
#         self.serial_num = serial_num
#         self.status = status
#
#     def get_time_act_status(self):
#         if self.status == "Active":
#             res_time = datetime.now() - self.dt_create
#         else:
#             res_time = 0
#         return res_time
#
#     def change_status(self, new_status):
#         self.status = new_status
#         self.dt_create = datetime.now()
#
#     def get_app_id(self):
#         return self.__id
#
#     def __str__(self):
#         return f"""
#         ID: {self.__id}
#         Дата создания: {self.dt_create}
#         Имя: {self.first_name}
#         Серийный номер: {self.serial_num}
#         Статус: {self.status}
#         """
#
#
# apl1 = Application('Dima', 241414, 'Active')
# apl2 = Application('Yura', 141516, 'New')
# apl3 = Application('Sergey', 178733, 'Closed')
# apl4 = Application('Oleg', 272252, 'New')
#
# # Получение информации по заявке
# print(apl1)
# print(apl2)
# print(apl3)
# print(apl4)
# # Пауза в 2 секунды
# time.sleep(1)
# # Изменение статуса по 4 заявке на Активный
# apl4.change_status("Active")
# # Повторный вывод общей информации о заявке, смотрим на изменения
# print(apl4)
#
#
# # Получение id заявки
# print(apl1.get_app_id())
# time.sleep(1)
# # Вывод времени жизни заявки в статусе Active, если другой статус то 0
# print(f"Время жизни заявки с id: {apl1.get_app_id()}:   {apl1.get_time_act_status()}")
# time.sleep(1)
# print(f"Время жизни заявки с id: {apl2.get_app_id()}:   {apl2.get_time_act_status()}")
# time.sleep(1)
# print(f"Время жизни заявки с id: {apl3.get_app_id()}:   {apl3.get_time_act_status()}")
# time.sleep(1)
# print(f"Время жизни заявки с id: {apl4.get_app_id()}:   {apl4.get_time_act_status()}")

#
# # Задание № 3
# class Matrix():
#     def __init__(self, matrix):
#         self.matrix = matrix
#
#     # Вывод матрицы на экран
#     def __str__(self):
#         # return '\n'.join(' '.join(map(str, row)) for row in self.matrix)
#         return '\n'.join([''.join(['%s\t' % i for i in row]) for row in self.matrix])
#
#     # Сложение
#     def __add__(self, other):
#
#         try:
#             res = []
#
#             for i in range(len(self.matrix)):
#                 i_res = []
#                 for j in range(len(self.matrix[0])):
#                     i_res.append(self.matrix[i][j] + other.matrix[i][j])
#                 res.append(i_res)
#             return  res
#
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#     # Умножение
#     def __mul__(self, num):
#
#         try:
#             res = []
#
#             for i in range(len(self.matrix)):
#                 i_res = []
#                 for j in range(len(self.matrix[0])):
#                     i_res.append(self.matrix[i][j] * num)
#                 res.append(i_res)
#
#             return res
#
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#     # Вычитание
#     def __sub__(self, other):
#         try:
#             res = []
#
#             for i in range(len(self.matrix)):
#                 i_res = []
#                 for j in range(len(self.matrix[0])):
#                     i_res.append(self.matrix[i][j] - other.matrix[i][j])
#                 res.append(i_res)
#             return res
#
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#     # Деление
#     def __truediv__(self, num):
#         try:
#             res = []
#
#             for i in range(len(self.matrix)):
#                 i_res = []
#                 for j in range(len(self.matrix[0])):
#                     i_res.append(self.matrix[i][j]/num)
#                 res.append(i_res)
#
#             return res
#
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#
# p1 = Matrix([[1, 2, 3],[4, 5, 6],[7, 8, 9]])
# p2 = Matrix([[8, 3, 9],[1, 6, 2],[4, 4, 3]])
# print(f'Матрица №1:\n{p1}')
# print(f'Матрица №2:\n{p2}')
#
# # Сложение
# print(f'Сложение:\n{Matrix(p1+p2)}')
# # Умножение
# print(f'Умножение:\n{Matrix(p1*2)}')
#
# # Вычитание
# print(f'Вычитание:\n{Matrix(p1-p2)}')
#
# # Деление
# print(f'Деление:\n{Matrix(p1/2)}')
