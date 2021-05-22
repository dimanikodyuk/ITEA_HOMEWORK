# Задание №1
import time

def my_func(count_v):
    print("Запуск основной функции")
    i = 0
    sum = 0
    br_point = True
    while br_point:
        i = i + 1
        sum = sum+i*i
        if i == count_v:
            br_point = False
        print(f'{i} \n')

    print(sum)


def outer(a):
    def timer_func(f):
        print("Начало выполнения основной функции")
        st_time = start_time = time.time()
        f(a)
        end_time = ("%s second" % (time.time() - st_time))
        print("Конец выполнения основной функции")
        print(f'Время выполнения функции: {end_time}')
    return timer_func

res = outer(50000)(my_func)



#Задание №2
# n1 = input("Укажите первое число ряда Фибоначчи: ")
# n1 = int(n1)
# n2 = input("Укажите второе число ряда Фибоначчи: ")
# n2 = int(n2)
# cou = input("Укажите номер искомого элемента ряда Фибоначчи: ")
# cou = int(cou)
#
# arr = []
# arr.append(n1)
# arr.append(n2)
#
# i = 0
# while i < cou -2:
#     fib = n1 + n2
#     n1 = n2
#     n2 = fib
#     arr.append(n2)
#     i = i + 1
#
# print(arr)
# print(f"Искомый элемент ряда Фибоначчи - {cou} , его значение: " + str(arr[cou-1]))

# Задание №3 Вариант 1
# def get_sum(a,b,c):
#     if a > b and a > c:
#         if b > c:
#             res = a + b
#         else:
#            res = a + c
#     elif b > a and b > c:
#         if a > c:
#             res = b + a
#         else:
#             res = b + c
#     elif c > a and c > b:
#         if a > b:
#             res = c + a
#         else:
#             res = c + b
#     # Если все числа равны между собой
#     elif a == b and b == c:
#         res = a + b
#     return res
#
# try:
#     n1 = input("Укажите первое число: ")
#     n1 = int(n1)
#     n2 = input("Укажите второе число: ")
#     n2 = int(n2)
#     n3 = input("Укажите третье число: ")
#     n3 = int(n3)
#
#     print(get_sum(n1,n2,n3))
#
# except ValueError as err:
#     print(f'Это не число. Ошибка: {err}')
# except Exception as err:
#     print(f'Произошла ошибка: {err}')


# Задание №3 Вариант 2
# try:
#     n1 = input("Укажите первое число: ")
#     n1 = int(n1)
#     n2 = input("Укажите второе число: ")
#     n2 = int(n2)
#     n3 = input("Укажите третье число: ")
#     n3 = int(n3)
#
#     arr = []
#     # Добавляем элементы в список
#     arr.append(n1)
#     arr.append(n2)
#     arr.append(n3)
#
#     # создаем отсортированный список
#     sort_arr = sorted(arr)
#
#     # Проверяем, если все числа между собой равны, то находим сумму первых двух
#     if arr[0] == arr[1] and arr[1] == arr[2]:
#         sum = arr[0] + arr[1]
#         print(f"Сума наибольших чисел: {sum}")
#     # В другом случае находим сумму последних двух чисел отсортированных в порядке увеличения
#     else:
#         sum = sort_arr[1] + sort_arr[2]
#         print(f"Сума наибольших чисел: {sum}")
# except ValueError as err:
#     print(f'Это не число. Ошибка: {err}')
# except Exception as err:
#     print(f'Произошла ошибка: {err}')

# Задание №4
# condition = True
# sum_num = 0
# while condition:
#
#     line = input("Укажите ряд чисел через пробел: ")
#     num = line.split(' ')
#
#     for n in num:
#         try:
#             if n.isnumeric() == False:
#                 condition = False
#             sum_num += int(n)
#         except ValueError as err:
#             print(f'Введено не число или спец. символ, заканчиваем работу программы: {err}')
#         except Exception as err:
#             print(f'Произошла ошибка: {err}')
#     print(f"Сумма введенных чисел :{sum_num}")