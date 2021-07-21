# write your code here
import os
import sys


def check_directory():
    args = sys.argv
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        print("Directory is not specified")
        exit()
    else:
        pass


def obtaining_data_list(file_extension):
    lst = []
    for root, dirs, files in os.walk('.', topdown=True):
        for name in files:
            lst.append(os.path.join(root, name))
    if file_extension != "":
        lst = [x for x in lst if file_extension in os.path.splitext(x)[1][1:]]
    else:
        lst = [x for x in lst if os.path.splitext(x)[1][1:] != ""]
    print("")
    return lst


def sort_list(sizes):
    sort_by = int(input("""Size sorting options:
1. Descending
2. Ascending\n"""))
    if sort_by == 1:
        sizes = sorted(sizes, reverse=True)
        return sizes
    elif sort_by == 2:
        sizes = sorted(sizes, reverse=False)
        return sizes
    else:
        print("\nWrong option")
        sort_list(sizes)


def creating_sorted_dict(data_list):
    file_sizes = sort_list(list(set(os.path.getsize(x) for x in data_list)))
    paths_dict = dict.fromkeys(file_sizes, [])
    # paths_dict = dict.fromkeys(sort_list(list(set(os.path.getsize(x) for x in data_list))), [])
    for x in paths_dict:
        paths_dict[x] = [y for y in data_list if str(x) == str(os.path.getsize(y))]
    return paths_dict


def print_results(paths_dict):
    print()
    for x in paths_dict:
        if len(paths_dict[x]) > 1:
            print(int(x), "bytes")
            for y in paths_dict[x]:
                if len(y) > 1:
                    print(y)
            print()
    print()


def main():
    check_directory()
    full_data = obtaining_data_list(input("Enter the file format:\n"))
    paths_dict = creating_sorted_dict(full_data)
    print_results(paths_dict)


if __name__ == "__main__":
    main()
