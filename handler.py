import os
import sys
import hashlib


def root_dir_check():
    """this function checks whether the directory argument provided and
    continues execution fun main()  or prints an error message & exit the program"""
    args = sys.argv
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        print("Directory is not specified")
        exit()


def obtaining_data_list(extension="", abs_paths_lst=[]) -> list:
    """ this function scans provided directory and creates the list of absolut paths to all files in directory
    if arg extension is empty - all paths kept, else - lst will keep only paths to files with a specified extension
    returns filtered list of absolut paths to all files with the requested extension in directory"""
    print("")
    for root, dirs, files in os.walk(r'./module/', topdown=True):
        """it's important to start with ./module folder, to ensure that no system JetBrains files in dataset"""
        for name in files:
            abs_paths_lst.append(os.path.join(root, name))
    if extension != "":
        # try to implement filter function
        abs_paths_lst = [x for x in abs_paths_lst if os.path.splitext(x)[1][1:] == extension]
    else:
        abs_paths_lst = [x for x in abs_paths_lst if os.path.splitext(x)[1][1:] != ""]
    return abs_paths_lst


def creating_data_dict(data_list: list) -> dict:
    """this function takes a filtered list of absolut paths, produced by obtaining_data_list() function
    create a list of unique file sizes and creates and empty dict using the list of sizes as keys
    appends lists of paths values to their keys in paths_dict
    calls sort_dictionary function and returns sorted dict of file sizes as keys and lists of absolut paths as values"""

    size_path_dict = dict.fromkeys([os.path.getsize(x) for x in data_list], [])
    for size in size_path_dict:
        size_path_dict[size] = [path for path in data_list if str(size) == str(os.path.getsize(path))]
    return size_path_dict


def sort_dictionary(data_dictionary: dict, reverse_status={1: True, 2: False}) -> dict:
    """this function takes list of file sizes and sort it in Descending or Ascending order
    returns sorted list with file sizes as stings"""

    sort_option = int(input("Size sorting options:\n1. Descending\n2. Ascending\n"))
    if sort_option not in reverse_status:
        print("\nWrong option")
        return sort_dictionary(data_dictionary)
    else:
        dict_as_tuple = tuple(data_dictionary.items())
        sorted_tuple = sorted(dict_as_tuple, reverse=reverse_status[sort_option])
        sorted_dict = dict(sorted_tuple)
        sorted_dict = {str(key): value for key, value in sorted_dict.items()}
        return sorted_dict


def print_results(data_dictionary):
    """this function prints the output(result) of the program. if a format key: \n values"""
    print()
    for key, value in data_dictionary.items():
        print()
        print(key, "bytes\n")
        print(*value, sep="\n")


def obtain_hash(file) -> hash:
    """reads 'file' in a binary mode, calculates it's md5-hash value and returns value converted into hex-digit format"""
    with open(file, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()


def check_for_duplicates(data_dictionary) -> dict:
    check = input("\nCheck for duplicates? (yes, no)\n").lower()
    if check == "yes":
        for key, value in data_dictionary.items():
            data_dictionary[key] = {obtain_hash(x): [y for y in value if obtain_hash(y) == obtain_hash(x) if len(value) > 1] for x in value}
        return data_dictionary


def print_duplicates111111(size_hash_dictionary) -> dict:
    """this function prints the output(result) of the program. if a format key: \n values"""
    del_dict = {}
    i = 1
    print()
    for key in size_hash_dictionary:
        print()
        print(key, "bytes\n")
        for file_hash in size_hash_dictionary[key]:
            if len(size_hash_dictionary[key][file_hash]) > 1:
                print("Hash:", file_hash)
                for path in size_hash_dictionary[key][file_hash]:
                    print(f"{i} {path}")
                    del_dict[str(i)] = path
                    i += 1
    print()
    return delete_files(del_dict)


def print_duplicates(size_hash_dictionary) -> dict:
    """this function prints the output(result) of the program. if a format key: \n values"""
    del_dict = {}
    i = 1
    print()
    for file_size, file_hashes in size_hash_dictionary.items():
        print()
        print(file_size, "bytes\n")
        for file_hash in file_hashes:
            if len(file_hashes[file_hash]) > 1:
                print("Hash:", file_hash)
                for file_path in file_hashes[file_hash]:
                    print(i, file_path)
                    del_dict[i] = file_path
                    i += 1

    print()
    return delete_files(del_dict)



def delete_files(dl_dict) -> int:
    decision = input("Delete files?")
    if decision.lower() not in {"yes", "no"}:
        print("Wrong option")
        return delete_files(dl_dict)
    else:
        while True:
            file_numbers = input("Enter file numbers to delete:\n").split(" ")
            try:
                file_numbers = [int(number) for number in file_numbers]
                file_numbers = sorted(file_numbers, reverse=True)
            except ValueError:
                print("Wrong format")
            else:
                print(len(dl_dict))
                if file_numbers[0] not in dl_dict.keys():
                    print("Wrong format")
                else:
                    freed_stace = 0
                    for nmbr in file_numbers:
                        freed_stace += int(os.path.getsize(dl_dict[nmbr]))
                        os.remove(dl_dict[nmbr])
                    print(f"Total freed up space: {freed_stace} bytes")
                    break


def del_dpl(duplicates_dict):
    duplicates_dict = {key: value for key, value in duplicates_dict.items()}

    nd = {key: [] for key in duplicates_dict.keys()}
    for key, value in duplicates_dict.items():
        for subvalue in value:
            if len(value[subvalue]) >= 2:
                nd[key].append(value)

    print(nd)

if __name__ == "__main__":
    """this is the main function which calls other functions in a defined order"""
    root_dir_check()
    full_data = obtaining_data_list(input("Enter the file format:\n"))
    paths_dict = creating_data_dict(full_data)
    sorted_paths_dict = sort_dictionary(paths_dict)
    print_results(sorted_paths_dict)
    duplicates_dict = check_for_duplicates(sorted_paths_dict)


    #duplicates_dict = del_dpl(duplicates_dict)

    print_duplicates(duplicates_dict)
