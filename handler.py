# write your code here
import os
import sys

args = sys.argv

def sort_list(sizes):
    sort_by = int(input("""Size sorting options:
1. Descending
2. Ascending\n"""))
    if sort_by == 1:
        sizes = sorted(sizes, reverse=True)
        sizes = [str(x) for x in sizes]
    elif sort_by == 2:
        sizes = sorted(sizes, reverse=False)
        sizes = [str(x) for x in sizes]
    else:
        print("\nWrong option")
        sort_list(sizes)


def print_results(test_dict):
    for x in test_dict:
        if str(x) != '0':
            print(int(x) * 1000, "bytes")
            for y in test_dict[x]:
                print(y if len(y) > 2 else "error")
            print()


def check_directory():
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        print("Directory is not specified")
    else:
        return main()


def main():
    folder = args[1]
    format = input("Enter file format:\n")
    sizes = []
    for root, dirs, files in os.walk('.', topdown=True):
        if len(format) > 0:
            for name in files:
                if str(os.path.splitext(name)[1]) == format[1:]:
                    sizes.append(os.path.getsize(os.path.join(root, name)))
                sizes = list(set(sizes))
                sizes = [str(x) for x in sizes]  # test str
        else:
            for name in files:
                sizes.append(os.path.getsize(os.path.join(root, name)))
            sizes = list(set(sizes))
            sizes = [str(x) for x in sizes]  # test str

    sort_list(sizes)
    test_dict = dict.fromkeys(sizes, [])

    for root, dirs, files in os.walk('.', topdown=True):
        for name in files:
            full_path = os.path.join(root, name)
            size = os.path.getsize(full_path)
            # full_data.append([full_path, size])
            for x in test_dict:
                if str(os.path.getsize(full_path)) == x and x in test_dict:
                    test_dict[x].append(os.path.join(root, name))
                    # can make sort of lists in dict
                    # issue is that filter doesn't work. all files are appended to all dict keys

    #for x in test_dict:
    #    for y in full_data:
    #        test_dict[x] = [y[0].lower() for y in full_data if str(y[1]) == str(x)]

    print_results(test_dict)


check_directory()

#print(os.path.getsize('./module/root_folder/calc/server.php'))
#print(os.path.getsize("./handler.py"))
