import os
import sys
import hashlib


def check_directory():
    # this function checks whether the directory argument provided and
    # continues execution fun main()  or prints an error message & exit the program
    args = sys.argv
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        print("Directory is not specified")
        exit()


def obtaining_data_list(extension):
    # this function scans provided directory and creates the list of absolut paths to all files in directory
    # if arg extension is empty - all paths kept, else - lst will keep only paths to files with a specified extension
    lst = []

    for root, dirs, files in os.walk('.', topdown=True):
        for name in files:
            lst.append(os.path.join(root, name))
    if extension != "":
        lst = [x for x in lst if extension == os.path.splitext(x)[1][1:]]
    else:
        lst = [x for x in lst if os.path.splitext(x)[1][1:] != ""]
    print("")
    # returns a filtered list of absolut paths to all files with the requested extension in directory
    return lst


def sort_list(sizes):
    # this function takes list of file sizes and sort it in Descending or Ascending order
    # returns sorted list with file sizes as stings
    sort_by = int(input("""Size sorting options:
1. Descending
2. Ascending\n"""))
    if sort_by == 1:
        sizes = sorted(sizes, reverse=True)
        return [str(x) for x in sizes]  # converting file sizes to str
    elif sort_by == 2:
        sizes = sorted(sizes, reverse=False)
        return [str(x) for x in sizes]   # converting file sizes to str
    else:
        print("\nWrong option")
        return sort_list(sizes)


def creating_sorted_dict(data_list):
    # this function takes a filtered list of absolut paths, produced by obtaining_data_list() function
    # create a list of unique file sizes and creates and empty dict using the list of sizes as keys
    # appends lists of paths values to their keys in paths_dict
    file_sizes = list(set(os.path.getsize(x) for x in data_list))  # converting to set and back to list - removes all duplicates
    file_sizes = sort_list(file_sizes)
    paths = dict.fromkeys(file_sizes, [])
    for size in paths:
        paths[size] = [path for path in data_list if str(size) == str(os.path.getsize(path))]
        # returns dict of file sizes as keys and lists of absolut paths as values
    return paths


def print_results():
    # this function prints the output(result) of the program. if a format key: \n values
    print()
    for x in paths_dict:
        if len(paths_dict[x]) > 1:
            print(int(x), "bytes")
            for y in paths_dict[x]:
                if len(y) > 1:
                    print(y)
            print()
    print()


def obtain_hash(file):
    with open(file, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()


def print_duplicates(size_hash_dictionary):
    # this function prints the output(result) of the program. if a format key: \n values
    i = 1
    print()
    for key in size_hash_dictionary:
        print(key, "bytes")
        for file_hash in size_hash_dictionary[key]:
            if len(size_hash_dictionary[key][file_hash]) > 1:
                print("Hash:", file_hash)
                for path in size_hash_dictionary[key][file_hash]:
                    print(f"{i} {path}")
                    i += 1
    print()


def check_for_duplicates():
    check = input("Check for duplicates? (yes, no)")
    if check.lower() == "yes":
        for key, value in paths_dict.items():
            paths_dict[key] = {obtain_hash(x): [y for y in value if obtain_hash(y) == obtain_hash(x) if len(value) > 1] for x in value}
        new_dict = {}
        for key in paths_dict:
            for x in paths_dict[key]:
                if len(paths_dict[key][x]) > 0:
                    new_dict[key] = paths_dict[key]
        print_duplicates(new_dict)
    else:
        # finish the program
        exit()


if __name__ == "__main__":
    # this is the main function which calls other functions in a defined order
    check_directory()
    file_extension = input("Enter the file format:\n")
    full_data = obtaining_data_list(file_extension)
    paths_dict = creating_sorted_dict(full_data)
    print_results()
    check_for_duplicates()
