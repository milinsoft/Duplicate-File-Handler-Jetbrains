# write your code here
import os
import sys

args = sys.argv


def size_sorting_options():
    global test_dict
    sort_by = int(input("""Size sorting options:
1. Descending
2. Ascending\n"""))
    if sort_by == 1:
        print("LINE# 14", type(test_dict))
        # bad way to sor test_dict, as it changes it's type to list. need to sort (sizes) or find another way to sort dict
        test_dict = sorted(test_dict, reverse=True)
        print("LINE# 16", type(test_dict))
        print(test_dict)
        for a in test_dict:
            print(a * 1000, "bytes")
            print(*test_dict)

    elif sort_by == 2:
        print("LINE# 22", type(test_dict))
        # bad way to sor test_dict, as it changes it's type to list. need to sort (sizes) or find another way to sort dict
        test_dict = sorted(test_dict, reverse=False)
        print("LINE# 24", type(test_dict))
        for a in test_dict:
            print(a * 1000, "bytes")
            print(type(test_dict))


    else:
        print("\nWrong option")
        size_sorting_options()


sizes = []
#test_dict = []
full_data = []

if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
    print("Directory is not specified")
else:
    folder = args[1]

    format = input("Enter file format:\n")
    if format:
        format = "." + format

    for root, dirs, files in os.walk(folder, topdown=True):
        if format:
            for name in files:
                #print(os.path.join(root, name), "size:", os.path.getsize(os.path.join(root, name)))
                if str(os.path.splitext(name)[1]) == format:
                    #full_path = os.path.join(root, name)
                    sizes.append(os.path.getsize(os.path.join(root, name)))
                sizes = list(set(sizes))
                sizes = [str(x) for x in sizes]  # STR CONVERTER TEST
                test_dict = dict.fromkeys(sizes, [])
        elif len(format) == 0:
            for name in files:
                sizes.append(os.path.getsize(os.path.join(root, name)))
            sizes = list(set(sizes))
            sizes = [str(x) for x in sizes]  # STR CONVERTER TEST
            test_dict = dict.fromkeys(sizes, [])
            print(type(test_dict))

    for root, dirs, files in os.walk(folder, topdown=True):
        for name in files:
            full_path = os.path.join(root, name)
            for x in test_dict:
                if x == os.path.getsize(full_path):
                    x.append(full_path)
    print(test_dict)

sort = size_sorting_options()
