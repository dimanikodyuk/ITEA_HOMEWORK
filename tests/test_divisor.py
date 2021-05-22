import pytest

# def divisor(a, b):
#     return a/b
#
# # декоратор, принимает на вход именование аргументов джля тестовой функции и их значения
# @pytest.mark.parametrize("delimoe, delitel, expected", [(1,2,0.5), (100,50,2)])
# def test_my_divisor_func(delimoe, delitel, expected):
#     res = divisor(delimoe, delitel)
#     # assert проверяет что выражение после него ИСТИНА
#     assert res == expected
#
#
# # менеджер контекста
# @pytest.mark.parametrize("exc_type, delimoe, delitel", [(ZeroDivisionError, 1, 0), (TypeError, "1", 3)])
# def test_divisor_with_error(exc_type, delimoe, delitel):
#     with pytest.raises(exc_type):
#         divisor(delimoe, delitel)


class Matrix():
    def __init__(self, matrix):
        self.matrix = matrix

    # Вывод матрицы на экран
    def print_matrix(self):
        for i in self.matrix:
            print(i)

    # Сложение

    def __add__(self, m1):
        print("\nРезультат сложения матриц:\n")
        try:
            res = []

            Matrix.print_matrix(self)
            print("+")
            Matrix.print_matrix(m1)
            print("=")

            for i in range(len(self.matrix)):
                i_res = []
                for j in range(len(self.matrix[0])):
                    i_res.append(self.matrix[i][j] + m1.matrix[i][j])
                res.append(i_res)
            return  Matrix(res)

        except Exception as err:
            print(f'Произошла ошибка: {err}')

    # Умножение
    def __mul__(self, num):
        print("\nРезультат умножения матриц:\n")
        try:

            res = []

            Matrix.print_matrix(self)
            print(f"* {num}")
            print("=")

            for i in range(len(self.matrix)):
                i_res = []
                for j in range(len(self.matrix[0])):
                    i_res.append(self.matrix[i][j] * num)
                res.append(i_res)

            return Matrix(res)
        except Exception as err:
            print(f'Произошла ошибка: {err}')

    # Вычитание
    def __sub__(self, m1):
        print("\nРезультат вычитания матриц:\n")
        try:
            res = []

            Matrix.print_matrix(self)
            print("-")
            Matrix.print_matrix(m1)
            print("=")

            for i in range(len(self.matrix)):
                i_res = []
                for j in range(len(self.matrix[0])):
                    i_res.append(self.matrix[i][j] - m1.matrix[i][j])
                res.append(i_res)
            return Matrix(res)

        except Exception as err:
            print(f'Произошла ошибка: {err}')


    # Деление
    def __divmod__(self, num):
        print("\nРезультат деления матрицы на число:\n")
        try:
            res = []

            Matrix.print_matrix(self)
            print(f"/ {num}")
            print("=")

            for i in range(len(self.matrix)):
                i_res = []
                for j in range(len(self.matrix[0])):
                    i_res.append(self.matrix[i][j]/num)
                res.append(i_res)

            return Matrix(res)

        except Exception as err:
            print(f'Произошла ошибка: {err}')


p1 = Matrix([[1,2,3],[4,5,6],[7,8,9]])
p2 = Matrix([[8,3,9],[1,6,2],[4,4,3]])
# p1.print_matrix()
# p2.print_matrix()

# # Сложение
# add_matrix = Matrix.__add__(p1,p2)
# add_matrix.print_matrix()
# # Умножение
mull_matrix = Matrix.__mul__(p1,2)
mull_matrix.print_matrix()
# Вычитание
# sub_matrix = Matrix.__sub__(p1,p2)
# sub_matrix.print_matrix()
# # Деление
# div_matrix = Matrix.__divmod__(p1, 2)
# div_matrix.print_matrix()



# # декоратор, принимает на вход именование аргументов джля тестовой функции и их значения
# @pytest.mark.parametrize("delimoe, delitel, expected", [(1,2,0.5), (100,50,2)])
# def test_my_divisor_func(delimoe, delitel, expected):
#     res = divisor(delimoe, delitel)
#     # assert проверяет что выражение после него ИСТИНА
#     assert res == expected
#
#
# # менеджер контекста
# @pytest.mark.parametrize("exc_type, delimoe, delitel", [(ZeroDivisionError, 1, 0), (TypeError, "1", 3)])
# def test_divisor_with_error(exc_type, delimoe, delitel):
#     with pytest.raises(exc_type):
#         divisor(delimoe, delitel)

data_1 = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

data_2 = [[8, 3, 9],
          [1, 6, 2],
          [4, 4, 3]]

data_add = [[9,5,12],
          [5,11,8],
          [11,12,12]]

data_mul = [[2,4,6],
            [8,10,12],
            [14,16,18]]

data_sub = [[-7, -1, -6],[3, -1, 4],[3, 4, 6]]

data_div = [[0.5,1,1.5],
            [2,2.5,3],
            [3.5,4,4.5]]



@pytest.mark.parametrize("matr1, matr2, deystive, result", [(data_1, data_2, "add", data_add),(data_1, data_2, "sub",data_sub),(data_1, 2, "div", data_div), (data_1, 2, "mul", data_mul)])
def test_my_matr(matr1, matr2, deystive, result):

    m1 = Matrix(data_1)
    m2 = Matrix(data_2)

    expected_data = result

    if deystive == "add":
        exp_matr = m1+m2
    elif deystive == "mul":
        exp_matr = m1*data_2
    elif deystive == "div":
        exp_matr = m1/data_2
    elif deystive == "sub":
        exp_matr = m1-m2

    assert expected_data == exp_matr.matrix

