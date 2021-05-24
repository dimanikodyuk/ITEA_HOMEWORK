# Задание №3

# Способ 1

def file_replace(old_file_path, new_file_path):
    try:
        new_list = []
        with open(old_file_path,'r') as f:
            old_data = f.read()
            new_list.append(old_data.replace('One','Один').replace('Two','Два').replace('Three','Три').replace('Four','Четыри'))

        with open(new_file_path,'w', encoding='utf-8') as f1:
            for i in new_list:
                f1.write(i)

    except FileNotFoundError as err:
        print(f"Ошибка с файлом: {err}")


# Способ 2

def file_replace_v2(old_file_path, new_file_path):
    try:
        new_list = []
        f = open('C:/Git/ITEA_HOMEWORK/homework_3/test_file.txt','r')
        for i in f.readlines():
            print(i)
            new_list.append(i.replace('One','Один').replace('Two','Два').replace('Three','Три').replace('Four','Четыри'))

        f1 = open('C:/Git/ITEA_HOMEWORK/homework_3/new_file.txt','w',  encoding='utf-8')
        for j in new_list:
            f1.write(j)
    except FileNotFoundError as err:
        print(f"Ошибка с файлом: {err}")


old_file = 'C:/Git/ITEA_HOMEWORK/homework_3/test_file.txt'
new_file = 'C:/Git/ITEA_HOMEWORK/homework_3/new_file.txt'

file_replace(old_file, new_file)
file_replace_v2(old_file, new_file)

