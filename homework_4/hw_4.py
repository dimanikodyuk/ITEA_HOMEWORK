# Задание №1

# Способ №1. Цикл for
def factorial(n):
    res = 1
    for j in range(1, n + 1):
        res *= j
        yield res

print("")
d = factorial(5)
print(next(d))
print(next(d))
print(next(d))
print(next(d))
print(next(d))

# Способ №2. Рекурсия
def factorial_rec(num):
        res = 1

        if num < 0:
            yield "Ошибка. Факториал можно найти только для положительных целых чисел"
        elif num == 0:
            yield 1
        else:
            for i in range (1, num + 1):
                res = res*i
            yield res

d = factorial_rec(5)
print(f"\nРезультат расчета факториала с помощью рекурсии: {next(d)}")




# Задание №2
from abc import ABC, abstractmethod

# Класс оргтехники
class Orgtechnik(ABC):
    def __init__(self, name, company, count, sales=False, in_stock=False):
        self.name = name
        self.company = company
        self.count = count
        self.sales = sales
        self.in_stock = in_stock

    # Абстрактный метод проверки товара на продажу
    @abstractmethod
    def check_sales(self):
        pass

    @abstractmethod
    def to_warehouse(self):
        pass

    # Перемещение на склад
    def to_warehouse(self):
        if self.in_stock == False:
            if self.count > 0:
                self.in_stock = True
                res = f'Внимание! Товар {self.name} перемещен на склад в количестве {self.count} шт.'
            else:
                res = f'Внимание! Товар {self.name} закончился. Перемещение невозможно.'
        else:
            res = f'Внимание! Товар {self.name} уже на складе в количестве {self.count} шт.'
        print(res)

    # Продажи товара
    def sale(self):
        if self.count == 0:
            res = f'Внимание! Весь товар {self.name} продан'
            self.sale = True

        else:
            self.count = self.count - 1
            res =  f"Товар {self.name} продан в количестве 1 шт. Остаток {self.count}"
        print(res)




class Printer(Orgtechnik):

    def __init__(self, name, type, company, count, in_stock, comment):
        super().__init__(name, company, count, in_stock)
        self.type = type
        self.comment = comment

    def check_sales(self):
        if self.sales == 0:
            res = 'Нет в наличии'
        else:
            res = 'Есть в наличии'
        return res

    def __str__(self):
        res = Printer.check_sales(self)
        res_text = f'''\nОписание принтера
----------------------------------------------
Название: {self.name}
Тип: {self.type}
Компания: {self.company}
Количество: {self.count}
Статус: {res}
Коментар: {self.comment}
----------------------------------------------
        '''
        return  res_text

    def add_comment(self, new_comment):
        self.comment = self.comment + '; ' + new_comment
        return self.comment

    def req_cartridge_repl(self):
        pass




class Scaner(Orgtechnik):
    def __init__(self,name, format, type, company, count, in_stock):
        super().__init__(name, company,  count, in_stock)
        self.format = format
        self.type = type

    def check_sales(self):
        if self.count == 0:
            res = 'Нет в наличии'
        else:
            res = 'Есть в наличии'
        return res



    def __str__(self):
        res = Scaner.check_sales(self)
        res_text = f'''\nОписание сканера
----------------------------------------------
Название: {self.name}
Формат: {self.format}
Тип: {self.type}
Компания: {self.company}
Количество: {self.count}
Статус: {res}
----------------------------------------------
        '''
        return res_text

class Warehouse():
    list_objects = []

    def add_object(self, data):
        self.list_objects.append(data)
        return f'Добавлен: {data}'

    def __iter__(self):
        count = 0
        for i in self.list_objects:
            yield f'{count}:{i}'
            count = count+1




printer1 = Printer("HP-1203","Цветной",'FinX', 331515151, 2, 'Товар БУ')

# Вывод информации о принтере
print(printer1)
# Продажа одного принтера
Orgtechnik.sale(printer1)
# Добавление коментария
Printer.add_comment(printer1, 'Трубется замена картриджа')
# Вывод информации о принтере
print(printer1)
# Добавление коментария
Printer.add_comment(printer1, 'Возможна скидка в 20%')
# Вывод информации о принтере
print(printer1)
# Продажа одного принтера
Orgtechnik.sale(printer1)
# Продажа одного принтера
Orgtechnik.sale(printer1)
# Вывод информации о принтере
print(printer1)



scaner1 = Scaner('Samsung-P420', 'A3', 'Black and white', 'Finx', 10, False)
# Вывод информации о сканере
print(scaner1)
# Продажа сканеров
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
Orgtechnik.sale(scaner1)
# Вывод информации о сканере
print(scaner1)
Orgtechnik.sale(scaner1)
# Вывод информации о сканере
print(scaner1)
Orgtechnik.sale(scaner1)
# Перемещение сканеров на склад
Orgtechnik.to_warehouse(scaner1)
# Повторная попытка перемещения сканеров на склад
Orgtechnik.to_warehouse(scaner1)



list_data = Warehouse()
# Вывод товаров со склада
print(list_data.list_objects)

# Добавление товаров на склад
list_data.add_object(printer1)
list_data.add_object(scaner1)

# Вывод товаров со склада через итератор
for i in list_data:
    print(i)


#print(list_data.list_objects)


