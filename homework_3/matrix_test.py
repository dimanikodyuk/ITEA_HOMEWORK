class Matrix():
    def __init__(self, matrix):
        self.matrix = matrix

    # Вывод матрицы на экран
    def print_matrix(self):
        for i in self.matrix:
            print(i)

    # Сложение

    def addition_matrix(self, m1):
        print("\nРезультат сложения матриц:\n")
        try:
            x = self.matrix
            y = m1.matrix
            if len(x) != len(y):
                print(f"Данные матрицы не могут быть сложены, размеры матриц не совпадают. Матрица А: {len(x)}, матрица Б: {len(y)}")
            else:
                m = len(x)
                n = len(x[1])
                # создание матрицы с 0 элеменатми определенного размера, для сложения матриц
                result = [[0 for y in range(m)] for x in range(n)]

                Matrix.print_matrix(self)
                print("+")
                Matrix.print_matrix(m1)
                print("=")

                for i in range(len(x)):
                    for j in range(len(x[0])):
                        result[i][j] = x[i][j] + y[i][j]
                # вывод результирующей матрицы
                for i in result:
                    print(i)
        except Exception as err:
            print(f'Произошла ошибка: {err}')

    # Умножение
    def multiplication_matrix(self, m1):
        print("\nРезультат умножения матриц:\n")
        try:
            x = self.matrix
            y = m1.matrix
            if len(x) != len(y):
                print(f"Данные матрицы не могут быть умножены, размеры матриц не совпадают. Матрица А: {len(x)}, матрица Б: {len(y)}")
            else:
                Matrix.print_matrix(self)
                print("*")
                Matrix.print_matrix(m1)
                print("=")

                m = len(x)
                n = len(x[1])
                result = [[0 for y in range(m)] for x in range(n)]
                for i in range(len(x)):
                    for j in range(len(y[0])):
                        for k in range(len(y)):
                            result[i][j] += x[i][k]*y[k][j]

                for i in result:
                    print(i)

        except Exception as err:
            print(f'Произошла ошибка: {err}')

    # Вычитание
    @staticmethod
    def subtraction_matrix(self, m1):
        print("\nРезультат вычитания матриц:\n")
        try:
            x = self.matrix
            y = m1.matrix
            if len(x) != len(y):
                print(
                    f"Данные матрицы не могут быть вычтены, размеры матриц не совпадают. Матрица А: {len(x)}, матрица Б: {len(y)}")
            else:
                m = len(x)
                n = len(x[1])
                # создание матрицы с 0 элеменатми определенного размера, для сложения матриц
                result = [[0 for y in range(m)] for x in range(n)]

                Matrix.print_matrix(self)
                print("-")
                Matrix.print_matrix(m1)
                print("=")

                for i in range(len(x)):
                    for j in range(len(x[0])):
                        result[i][j] = x[i][j] - y[i][j]
                # вывод результирующей матрицы
                for i in result:
                    print(i)
        except Exception as err:
            print(f'Произошла ошибка: {err}')


    # Деление
    def divide_matrix(self, num):
        print("\nРезультат деления матрицы на число:\n")
        try:
            x = self.matrix

            Matrix.print_matrix(self)
            print(f"/ {num}")
            print("=")

            m = len(x)
            n = len(x[1])
            result = [[0 for y in range(m)] for x in range(n)]

            for i in range(len(x)):
                for j in range(len(x[0])):
                    result[i][j] = x[i][j]/num


            # вывод результирующей матрицы
            for i in result:
                print(i)

        except Exception as err:
            print(f'Произошла ошибка: {err}')


p1 = Matrix([[1,2,3],[4,5,6],[7,8,9]])
p2 = Matrix([[8,3,9],[1,6,2],[4,4,3]])
p1.print_matrix()
p2.print_matrix()

# Сложение
Matrix.addition_matrix(p1,p2)
# Умножение
Matrix.multiplication_matrix(p1,p2)
# Вычитание
Matrix.subtraction_matrix(p1,p2)
# Деление
Matrix.divide_matrix(p1, 2)