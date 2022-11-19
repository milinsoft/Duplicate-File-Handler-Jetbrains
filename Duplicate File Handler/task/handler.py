import os
from sys import argv as args
from hashlib import md5
from os.path import getsize, join
from colorama import Fore, init

init(autoreset=True)


class File:

    def __init__(self, path, size):
        self.size = size
        self.path = path
        self.hash = None

    def compute_md5_hash(self) -> hash:
        """returns file's md5-hash value in hex-digit format"""
        with open(self.path, "rb") as file:
            self.hash = md5(file.read()).hexdigest()


class DuplicateFileHandler:

    def __init__(self):
        self.files_tuple: tuple = tuple()
        self.sort_option: bool or None = None
        self.result_dict: dict = {}

    def get_files_catalogue(self, extension=None):
        """recursively scans directory provided and creates the list of absolute paths filtering by extension"""
        #
        abs_paths_tuple = tuple(
            join(root, name)
            for root, dirs, files in os.walk(r"./module/", topdown=True)
            for name in files
            if not extension or name.endswith(extension)
        )

        file_sizes = tuple(getsize(path) for path in abs_paths_tuple)
        self.files_tuple = tuple(
            File(size=getsize(path), path=path) for path in abs_paths_tuple if file_sizes.count(getsize(path)) > 1
        )

        # calculating hashes only for potential duplicates
        for file in self.files_tuple:
            file.compute_md5_hash()


    def get_sorting_preference(self):
        reverse_status = {1: True, 2: False}
        sort_option = int(input("Size sorting options:\n1. Descending\n2. Ascending\n"))
        if sort_option not in reverse_status:
            print("\nWrong option")
            return self.get_sorting_preference()
        self.sort_option = reverse_status[sort_option]
        # sort for correct final print
        self.files_tuple = tuple(
            sorted(self.files_tuple, key=lambda f: (f.size, f.hash), reverse=self.sort_option)
        )

    def print_same_size_files(self):
        file_size = None
        for file in self.files_tuple:
            # making sure size is printed only once
            if file_size != file.size:
                file_size = file.size
                print(f"\n{file_size:_} bytes\n")
            print(file.path)

    def get_duplicate_files(self):
        # removing objects with unique hash from the list as those are definitely not a duplicate!
        file_hashes = tuple(file.hash for file in self.files_tuple)
        self.files_tuple = tuple(filter(lambda x: file_hashes.count(x.hash) > 1, self.files_tuple))


    def check_for_duplicates(self):
        check = input("\nCheck for duplicates? (yes, no)\n").lower()
        if check == "yes":
            files_size_list = sorted((file.size for file in self.files_tuple), reverse=self.sort_option)
            sizes_with_several_files = [x for x in files_size_list if files_size_list.count(x) > 1]
            self.files_tuple = [file for file in self.files_tuple if file.size in sizes_with_several_files]
            
            # calculate hashes
            for file in self.files_tuple:
                file.compute_md5_hash()

    def print_duplicate_files(self):
        """this function prints the output(result) of the program. if a format key: \n values"""

        # removing objects with unique hash from the list as those are definitely not a duplicate!
        file_hashes = tuple(file.hash for file in self.files_tuple)
        self.files_tuple = tuple(filter(lambda x: file_hashes.count(x.hash) > 1, self.files_tuple))


        del_dict = {}
        file_size = file_hash = None
        for i, file in enumerate(self.files_tuple, start=1):
            # making sure size is printed only once
            if file_size != file.size:
                file_size = file.size
                print(f"\n{file_size:_} bytes\n")
            if file_hash != file.hash:
                file_hash = file.hash
                print("Hash:", file_hash)

            print(f"{i}.", file.path)
            del_dict[i] = file
            i += 1
        print()
        if del_dict:
            return DuplicateFileHandler.delete_files(del_dict)
        else:
            msg = "No duplicates found"
            exit(
                print(
                    f"{Fore.GREEN}{msg}!"
                    if not self.file_extension
                    else f"{Fore.GREEN}{msg} with file extension {Fore.RED}{self.file_extension} {Fore.GREEN}!"
                )
            )

    @staticmethod
    def delete_files(dl_dict):
        decision = input("Delete files? (YES/NO): ")
        while decision.lower() not in {"yes", "no"}:
            print("Wrong option")
            return DuplicateFileHandler.delete_files(dl_dict)

        if decision.lower() == "yes":
            while True:
                file_numbers = input("Enter file numbers to delete separated by space:\n").split(" ")
                try:
                    file_numbers = sorted([int(number) for number in file_numbers], reverse=True)
                    # checking the biggest index if it exists - all other too!
                    if file_numbers[0] not in dl_dict.keys():
                        raise ValueError
                except ValueError:
                    print("Wrong option")
                else:
                    freed_space = 0
                    for number in file_numbers:
                        freed_space += dl_dict[number].size
                        os.remove(dl_dict[number].path)
                    print(f"{Fore.GREEN}Total freed up space: {freed_space:_} bytes")
                    break

    def start(self):
        """this is the main function which calls other functions in a defined order"""
        self.get_files_catalogue(input("Enter the file format or press 'return' for all:\n"))
        self.get_sorting_preference()
        self.print_same_size_files()
        self.get_duplicate_files()
        self.check_for_duplicates()
        self.print_duplicate_files()


if __name__ == "__main__":
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        exit(print("Directory is not specified"))

    handler = DuplicateFileHandler()
    handler.start()
