import os
import os.path

test_list = []
test_pathes = ['./module/root_folder/phones.csv',
                './module/root_folder/info.txt',
                './module/root_folder/python.txt',
                './module/root_folder/lost.json',
                './module/root_folder/calc/server.php',
                './module/root_folder/calc/bikeshare.csv',
                './module/root_folder/project/index.html',
                './module/root_folder/project/extraversion.csv',
                './module/root_folder/project/python_copy.txt',
                './module/root_folder/files/some_text.txt',
                './module/root_folder/files/db_cities.js',
                './module/root_folder/files/stage/cars.json',
                './module/root_folder/files/stage/package-lock.json',
                './module/root_folder/files/stage/src/src.txt',
                './module/root_folder/files/stage/src/spoiler.js']

#print(test_pathes)

#format = "txt"
format = input("enter format like php, csv, html, csv, txt, js, json\n")
#for x in test_pathes:
#    extension = os.path.splitext(x)[1][1:]
#    print(extension)
#    format_filter = lambda x: x == format
#    test_list.append(list(filter(format_filter, extension)))
#print(test_list)

new_list = []
for x in test_pathes:
    extension = os.path.splitext(x)[1][1:]
    if extension == format:
        new_list.append(x)
print()
#print(new_list)
for x in new_list:
    print(x)
