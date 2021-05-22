# Задание №3

# Способ 1
new_list = []
with open('C:/Git/ITEA_HOMEWORK/homework_3/test_file.txt','r') as f:
    old_data = f.read()
    new_list.append(old_data.replace('One','Один').replace('Two','Два').replace('Three','Три').replace('Four','Четыри'))

with open('C:/Git/ITEA_HOMEWORK/homework_3/new_file.txt','w', encoding='utf-8') as f1:
    for i in new_list:
        f1.write(i)

# Способ 2

# new_list = []
# f = open('C:/Git/ITEA_HOMEWORK/homework_3/test_file.txt','r')
# for i in f.readlines():
#     print(i)
#     new_list.append(i.replace('One','Один').replace('Two','Два').replace('Three','Три').replace('Four','Четыри'))
#
# f1 = open('C:/Git/ITEA_HOMEWORK/homework_3/new_file.txt','w',  encoding='utf-8')
# for j in new_list:
#     f1.write(j)
