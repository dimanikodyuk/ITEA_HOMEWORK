# Задание №1
import time

# 1-я функция для теста
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
        #print(f'{i} \n')

    print(sum)

# 2-я функция для теста
def my_test(a, b, c):
    res = a+b
    time.sleep(1)
    res = res + c
    return res


def outer(*args, **kwargs):
    def timer_func(f):
        print("Начало выполнения основной функции")
        st_time = time.time()
        time.sleep(1)
        def inner(*fargs, **fkwargs):
            f(*fargs, **fkwargs)
        end_time = ("%s second" % (time.time() - st_time))
        print("Конец выполнения основной функции")
        print(f'Время выполнения функции {f}: {end_time} \n')
        return inner
    return timer_func


res  = outer(500000,2)(my_func)
res1 = outer(1,2,3,4,5)(my_test)



#Задание №2

def Fibonacci(check_num):
    try:
        arr = [0, 1]
        n1 = arr[0]
        n2 = arr[1]

        i = 0
        while i < check_num -2:
            fib = n1 + n2
            n1 = n2
            n2 = fib
            arr.append(n2)
            i = i + 1

        return arr[check_num-1]

    except ValueError as err:
        print(f'Это не число. Ошибка: {err}')
    except Exception as err:
        print(f'Произошла ошибка: {err}')

num = 5
res = Fibonacci(num)
print(f"Искомый элемент ряда Фибоначчи - {num} , его значение: {res}")



# Задание №3 Вариант 1
def get_sum(a,b,c):
    num_list = [a,b,c]

    try:
        num, index = min((num, index) for (index, num) in enumerate(num_list))
        num_list.pop(index)
        return sum(num_list)

    except ValueError as err:
        print(f'Это не число. Ошибка: {err}')
    except Exception as err:
        print(f'Произошла ошибка: {err}')

res = get_sum(11,5,89)
print(f"Сума наибольших чисел равна: {res}")

# Задание №4
condition = True
sum_num = 0
while condition:

    line = input("Укажите ряд чисел через пробел: ")
    num = line.split(' ')

    for n in num:
        try:
            if n.isnumeric() == False:
                condition = False
            sum_num += int(n)
        except ValueError as err:
            print(f'Введено не число или спец. символ, заканчиваем работу программы: {err}')
        except Exception as err:
            print(f'Произошла ошибка: {err}')
    print(f"Сумма введенных чисел :{sum_num}")