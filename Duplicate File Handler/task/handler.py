import os
from sys import argv as args
from hashlib import md5
from os.path import getsize, join

from collections import namedtuple


class DuplicateFileHandler:

    def obtaining_abs_paths_lst(self, extension=None) -> list:
        """ this function scans provided directory and creates the list of absolut paths to all files in directory
        if arg extension is empty - all paths kept, else - lst will keep only paths to files with a specified extension
        returns filtered list of absolut paths to all files with the requested extension in directory"""

        def correct_extension(filename) -> bool:
            return not extension or filename.endswith(extension)

        abs_paths_lst = [
            join(root, name)
            for root, dirs, files in os.walk(r"./module/", topdown=True)
            for name in files
            if correct_extension(name)
        ]
        return abs_paths_lst


    def creating_data_dict(self, abs_paths_lst: list) -> dict:
        """this function takes a filtered list of absolut paths, produced by obtaining_abs_paths_lst() function
        create a list of unique file sizes and creates and empty dict using the list of sizes as keys
        appends lists of paths values to their keys in paths_dict
        calls sort_dictionary function and returns sorted dict of file sizes as keys and lists of absolut paths as values"""


        size_path_dict = dict.fromkeys([getsize(x) for x in abs_paths_lst], [])

        for size in size_path_dict:
            size_path_dict[size] = [path for path in abs_paths_lst if size == getsize(path)]
        return size_path_dict


    # TODO maybe make it inner function?
    def sort_dictionary(self, sizes_and_paths_dict: dict) -> dict:
        """this function takes list of file sizes and sort it in Descending or Ascending order
        returns sorted list with file sizes as stings"""

        reverse_status = {1: True, 2: False}
        sort_option = int(input("Size sorting options:\n1. Descending\n2. Ascending\n"))
        if sort_option not in reverse_status:
            print("\nWrong option")
            return self.sort_dictionary(sizes_and_paths_dict)

            #TODO USE namedtuple instead?

        else:
            # Can be handy in case of getting rid of extra dict (by size)
            # sorted_dict = dict(sorted(sizes_and_paths_dict.items(), key=lambda x: x[1], reverse=reverse_status[sort_option]))
            return dict(sorted(sizes_and_paths_dict.items(), reverse=reverse_status[sort_option]))


    def print_search_results(self, sizes_and_paths_dict):
        """this function prints the output(result) of the program. if a format key: \n values"""
        for key, value in sizes_and_paths_dict.items():
            print(key, "bytes\n")
            print(*value, sep="\n")


    def check_for_duplicates(self, sizes_and_paths_dict) -> dict:

        def get_hash(file) -> hash:
            """reads 'file' in a binary mode, calculates it's md5-hash value and returns value converted into hex-digit format"""
            with open(file, 'rb') as file:
                return md5(file.read()).hexdigest()

        check = input("\nCheck for duplicates? (yes, no)\n").lower()
        sizes_hashes_and_path_dict = {}

        # checking only sizes with more than 2 keys
        sizes_and_paths_dict = dict(filter(lambda x: len(x[1]) > 1, sizes_and_paths_dict.items()))

        if check == "yes":
            for key, value in sizes_and_paths_dict.items():
                hash_and_path_dict = {get_hash(x): [path for path in value if get_hash(path) == get_hash(x)]
                                      for x in value}
                sizes_hashes_and_path_dict[key] = hash_and_path_dict

        return sizes_hashes_and_path_dict


    def print_duplicates(self, size_hash_dictionary):
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
        return self.delete_files(del_dict)


    def delete_files(self, dl_dict) -> int:
        decision = input("Delete files?")
        if decision.lower() not in {"yes", "no"}:
            print("Wrong option")
            return self.delete_files(dl_dict)

        elif decision.lower() == "no":
            exit()

        else:
            while True:
                file_numbers = input("Enter file numbers to delete separated by space:\n").split(" ")
                try:
                    file_numbers = sorted([int(number) for number in file_numbers], reverse=True)
                    if file_numbers[0] not in dl_dict.keys():
                        raise ValueError
                except ValueError:
                    print("Wrong format")
                else:
                    freed_space = 0
                    for number in file_numbers:
                        freed_space += int(getsize(dl_dict[number]))
                        os.remove(dl_dict[number])
                    print(f"Total freed up space: {freed_space} bytes")
                    break


    def start(self):
        full_data = self.obtaining_abs_paths_lst(input("Enter the file format:\n"))


        paths_dict = self.creating_data_dict(full_data)
        paths_dict = self.sort_dictionary(paths_dict)
        self.print_search_results(paths_dict)
        self.duplicates_dict = self.check_for_duplicates(paths_dict)
        self.print_duplicates(self.duplicates_dict)


if __name__ == "__main__":
    """this is the main function which calls other functions in a defined order"""
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        exit(print("Directory is not specified"))

    handler = DuplicateFileHandler()
    handler.start()
