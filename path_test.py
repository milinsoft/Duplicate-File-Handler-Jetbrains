import os
import os.path

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
                './module/root_folder/files/stage/src/spoiler.js',
                './module/root_folder/files/stage/src/this_path_is_without_format']

#print(test_pathes)

#format = "txt"

#for x in test_pathes:
#    extension = os.path.splitext(x)[1][1:]
#    print(extension)
#    format_filter = lambda x: x == format
#    test_list.append(list(filter(format_filter, extension)))
#print(test_list)

def first_method():
    format = input("enter format like php, csv, html, csv, txt, js, json\n")
    new_list = []
    for x in test_pathes:
        extension = os.path.splitext(x)[1][1:]
        if extension == format:
            new_list.append(x)
    print()
    #print(new_list)
    for x in new_list:
        print(x)

# filtering method
def second_method():
    format = input("enter format like php, csv, html, csv, txt, js, json\n")
    #format = "js"
    new_list = test_pathes
    new_list = list(filter(lambda x: os.path.splitext(x)[1][1:] == format, new_list))
    #print(os.path.splitext(new_list)[1][1:])
    #print(test_pathes)
    #os.path.splitext(x)[1][1:]
    print("")
    #print(new_list)
    for x in new_list:
        print(x)


def third_method():
    format = input("enter format like php, csv, html, csv, txt, js, json\n")
    new_list = test_pathes
    new_list = [x for x in new_list if os.path.splitext(x)[1][1:] == format]
    print("")
    #print(new_list)
    for x in new_list:
        print(x)


# work with dict
def fourth_method():
    format = input("enter format like php, csv, html, csv, txt, js, json\n")
    #print(type(format))
    #print(format == "")
    new_list = test_pathes
    if format != "":
        new_list = [x for x in new_list if format in os.path.splitext(x)[1][1:]]
    else:
        new_list = [x for x in new_list if os.path.splitext(x)[1][1:] != ""]
    print("")
    #print(new_list)
    for x in new_list:
        print(x)



#first_method()  # working
#second_method()  # working
#third_method()  # working
fourth_method()
