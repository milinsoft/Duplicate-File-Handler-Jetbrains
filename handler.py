# write your code here
import os
import sys


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


def check_directory():
    args = sys.argv
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        print("Directory is not specified")
    else:
        return main()


def full_data_filter(lst, file_format):
    if file_format != "":
        lst = [x for x in lst if file_format in os.path.splitext(x)[1][1:]]
    else:
        lst = [x for x in lst if os.path.splitext(x)[1][1:] != ""]
    print("")
    return lst


def main():
    file_format = input("Enter file file_format:\n")
    full_data = []
    for root, dirs, files in os.walk('.', topdown=True):
        for name in files:
            full_data.append(os.path.join(root, name))

    full_data = full_data_filter(full_data, file_format)  # filtering the list + returning new list, + assigning it to variable
    file_sizes = sort_list(list(set(os.path.getsize(x) for x in full_data)))  # sorting list with data.
    # creating dict using sizes list as keys
    paths_dict = dict.fromkeys(file_sizes, [])

    for x in paths_dict:
        paths_dict[x] = [y for y in full_data if str(x) == str(os.path.getsize(y))]
    print_results(paths_dict)


if __name__ == "__main__":
    check_directory()
