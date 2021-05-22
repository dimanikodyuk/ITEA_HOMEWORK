
# Задание №1

MAX_WORK_CAR_SPEED = 40
MAX_TOWN_CAR_SPEED = 60

class Car():
    car_counter = 0

    def __init__(self, speed, color, name, is_police):
        Car.car_counter += 1
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

    def go(self):
        return f"Машина {self.name} поехала"

    def stop(self):
        return f"Машина {self.name} остановилась"

    def show_speed(self):
        return self.speed

    def turn(self, direction):
        if direction == "left":
            res = f"Поворот машины {self.name} налево"
        elif direction == "right":
            res = f"Поворот машины {self.name} направо"
        elif direction == "back":
            res = f"Машина {self.name} развернулась"
        else:
            res = f"Машина {self.name} укатилась в неизвестном направлении"
        return res

    def show_car_info(self):
        res = f"""   \n    Описание автомобиля {self.name}:
    -------------------------------------------------------------------------------------
    Цвет: {self.color}.
    Скорость: {self.show_speed()} км/ч.
    -------------------------------------------------------------------------------------
        """
        return res

    @classmethod
    def show_car_counter(cls):
        return cls.car_counter

class TownCar(Car):

    def show_speed(self):
        if self.speed > MAX_TOWN_CAR_SPEED:
            return f"Автомобить {self.name} превысил скорость в классе TownCar на {self.speed - MAX_TOWN_CAR_SPEED} км/ч. Текущая скорость {self.speed}"
        else:
            return self.speed

class SportCar(Car):
    pass

class WorkCar(Car):

    def show_speed(self):
        if self.speed > MAX_WORK_CAR_SPEED:
            return f"Автомобить {self.name} превысил скорость в классе WorkCar на {self.speed - MAX_WORK_CAR_SPEED} км/ч. Текущая скорость {self.speed}"
        else:
            return self.speed

class PoliceCar(Car):
    pass

my_car1 = Car(120,"red","Ford",False)
my_car2 = TownCar(80, "white", "Renault", True)
my_car3 = SportCar(250, "black", "Suzuki", False)
my_car4 = WorkCar(41, "purple", "Honda", False)
my_car5 = PoliceCar(210, "white", "Lamborgini", True)

print(my_car3.go())
print(my_car3.turn("left"))
print(my_car3.turn("back"))
print(my_car3.stop())

print(my_car1.show_car_info())
print(my_car2.show_car_info())
print(my_car3.show_car_info())
print(my_car4.show_car_info())
print(my_car5.show_car_info())

#
# # Задание № 2
# import uuid
# import time
# from datetime import datetime
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
#     def get_apl_info(self):
#         res = f"""
#         ID: {self.__id}
#         Дата создания: {self.dt_create}
#         Имя: {self.first_name}
#         Серийный номер: {self.serial_num}
#         Статус: {self.status}
#         """
#         return res
#
# apl1 = Application('Dima', 241414, 'Active')
# apl2 = Application('Yura', 141516, 'New')
# apl3 = Application('Sergey', 178733, 'Closed')
# apl4 = Application('Oleg', 272252, 'New')
#
# # Получение информации по заявке
# print(apl1.get_apl_info())
# print(apl2.get_apl_info())
# print(apl3.get_apl_info())
# print(apl4.get_apl_info())
# # Пауза в 2 секунды
# time.sleep(2)
# # Изменение статуса по 4 заявке на Активный
# apl4.change_status("Active")
# # Повторный вывод общей информации о заявке, смотрим на изменения
# print(apl4.get_apl_info())
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

# Задание 3

# class Matrix():
#     def __init__(self, matrix):
#         self.matrix = matrix
#
#     # Вывод матрицы на экран
#     def print_matrix(self):
#         for i in self.matrix:
#             print(i)
#
#     # Сложение
#
#     def addition_matrix(self, m1):
#         print("\nРезультат сложения матриц:\n")
#         try:
#             x = self.matrix
#             y = m1.matrix
#             if len(x) != len(y):
#                 print(f"Данные матрицы не могут быть сложены, размеры матриц не совпадают. Матрица А: {len(x)}, матрица Б: {len(y)}")
#             else:
#                 m = len(x)
#                 n = len(x[1])
#                 # создание матрицы с 0 элеменатми определенного размера, для сложения матриц
#                 result = [[0 for y in range(m)] for x in range(n)]
#
#                 Matrix.print_matrix(self)
#                 print("+")
#                 Matrix.print_matrix(m1)
#                 print("=")
#
#                 for i in range(len(x)):
#                     for j in range(len(x[0])):
#                         result[i][j] = x[i][j] + y[i][j]
#                 # вывод результирующей матрицы
#                 for i in result:
#                     print(i)
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#     # Умножение
#     def multiplication_matrix(self, m1):
#         print("\nРезультат умножения матриц:\n")
#         try:
#             x = self.matrix
#             y = m1.matrix
#             if len(x) != len(y):
#                 print(f"Данные матрицы не могут быть сложены, размеры матриц не совпадают. Матрица А: {len(x)}, матрица Б: {len(y)}")
#             else:
#                 Matrix.print_matrix(self)
#                 print("*")
#                 Matrix.print_matrix(m1)
#                 print("=")
#
#                 m = len(x)
#                 n = len(x[1])
#                 result = [[0 for y in range(m)] for x in range(n)]
#                 for i in range(len(x)):
#                     for j in range(len(y[0])):
#                         for k in range(len(y)):
#                             result[i][j] += x[i][k]*y[k][j]
#
#                 for i in result:
#                     print(i)
#
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#     # Вычитание
#     @staticmethod
#     def subtraction_matrix(self, m1):
#         print("\nРезультат вычитания матриц:\n")
#         try:
#             x = self.matrix
#             y = m1.matrix
#             if len(x) != len(y):
#                 print(
#                     f"Данные матрицы не могут быть вычтены, размеры матриц не совпадают. Матрица А: {len(x)}, матрица Б: {len(y)}")
#             else:
#                 m = len(x)
#                 n = len(x[1])
#                 # создание матрицы с 0 элеменатми определенного размера, для сложения матриц
#                 result = [[0 for y in range(m)] for x in range(n)]
#
#                 Matrix.print_matrix(self)
#                 print("-")
#                 Matrix.print_matrix(m1)
#                 print("=")
#
#                 for i in range(len(x)):
#                     for j in range(len(x[0])):
#                         result[i][j] = x[i][j] - y[i][j]
#                 # вывод результирующей матрицы
#                 for i in result:
#                     print(i)
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#
#     # Деление
#     def divide_matrix(self, num):
#         print("\nРезультат деления матрицы на число:\n")
#         try:
#             x = self.matrix
#
#             Matrix.print_matrix(self)
#             print(f"/ {num}")
#             print("=")
#
#             m = len(x)
#             n = len(x[1])
#             result = [[0 for y in range(m)] for x in range(n)]
#
#             for i in range(len(x)):
#                 for j in range(len(x[0])):
#                     result[i][j] = x[i][j]/num
#
#
#             # вывод результирующей матрицы
#             for i in result:
#                 print(i)
#
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#
#
# p1 = Matrix([[1,2,3],[4,5,6],[7,8,9]])
# p2 = Matrix([[8,3,9],[1,6,2],[4,4,3]])
# p1.print_matrix()
# p2.print_matrix()
#
# # Сложение
# Matrix.addition_matrix(p1,p2)
# # Умножение
# Matrix.multiplication_matrix(p1,p2)
# # Вычитание
# Matrix.subtraction_matrix(p1,p2)
# # Деление
# Matrix.divide_matrix(p1, 2)