# Задание №3
# Способ 1

def file_replace(p_old_file_path, p_new_file_path, p_dict):
    try:
        f_old = open(p_old_file_path, 'r')
        f_new = open(p_new_file_path, 'w')

        is_end = 1
        while is_end:
            line = f_old.readline()
            if line != '':
                word_old = line.split()[0]
                line = line.replace(word_old, p_dict[word_old])
                f_new.write(line)
            else:
                is_end = 0
        f_old.close()
        f_new.close()
    except FileNotFoundError as err:
        print(f"Ошибка с файлом: {err}")


alpha_dict = {"One": "Один", "Two": "Два", "Three": "Три", "Four": "Четыри"}
old_file = 'test_file.txt'
new_file = 'new_file.txt'

file_replace(old_file, new_file, alpha_dict)

