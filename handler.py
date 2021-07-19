# write your code here
import os
import sys

#print(os.path.getsize("./module/root_folder/calc/server.php"))

def sort_list(sizes):
    sort_by = int(input("""Size sorting options:
1. Descending
2. Ascending\n"""))
    if sort_by == 1:
        sizes = sorted(sizes, reverse=True)
        sizes = [str(x) for x in sizes]  # changing value type int --> str only after sorting
        pass
    elif sort_by == 2:
        sizes = sorted(sizes, reverse=False)
        sizes = [str(x) for x in sizes]  # changing value type int --> str only after sorting
        #print(sizes)  # test print
        pass
    else:
        print("\nWrong option")
        sort_list(sizes)


def print_results(test_dict):
    for x in test_dict:
        if len(test_dict[x]) > 0:
            #print(int(x) * 1000, "bytes")
            print(int(x), "kilobytes")
            for y in test_dict[x]:
                print(y)
            #for y in test_dict[x]:
            #    if len(y) > 2:
            #        print(y)
            print()


def check_directory():
    args = sys.argv
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        print("Directory is not specified")
    else:
        return main()


def full_data_filter(lst, format):  # rename variable full_data to sizes
    if format != "":
        new_list = [x for x in lst if format in os.path.splitext(x)[1][1:]]
    else:
        new_list = [x for x in lst if os.path.splitext(x)[1][1:] != ""]
    print("")

    # test code
    #for x in new_list:
    #    print(x)
    return new_list


def main():
    format = input("Enter file format:\n")
    sizes = []
    full_data = []
    for root, dirs, files in os.walk('.', topdown=True):
        for name in files:
            full_path = os.path.join(root, name)
            full_data.append(full_path)

            #full_data = list(filter(lambda x: os.path.splitext(x[0])[1] == format, full_data))
            #print(full_data)
            #print(extension)
    new_list = full_data_filter(full_data, format)  # filtering the list + returning new list, + assigning it to variable
    sizes = [os.path.getsize(x) for x in new_list]
    sizes = list(set(sizes))
    #print(sizes)
    sort_list(sizes)  # sorting list with data.
    # creating dict using sizes list as keys
    test_dict = dict.fromkeys(sizes, [])

    for x in test_dict:
        test_dict[x] = [y.lower() for y in new_list if str(x) == str(os.path.getsize(y))]



    #print(test_dict)
    print_results(test_dict)


if __name__ == "__main__":  # running program only if it's called directly, not imported
   check_directory()
