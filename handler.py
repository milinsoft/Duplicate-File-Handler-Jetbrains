import os
from sys import argv as args
from hashlib import md5
from os.path import getsize, join


class File:

    def __init__(self, path, size):
        self.size = size
        self.path = path
        self.hash = None

    def get_hash(self) -> hash:
        """returns file's md5-hash value in hex-digit format"""
        with open(self.path, "rb") as file:
            self.hash = md5(file.read()).hexdigest()


class DuplicateFileHandler:

    def __init__(self):
        self.files_list: list = []
        self.sort_option: bool or None = None
        self.result_dict: dict = {}

    def get_files_list(self, extension=None):
        """recursively scans directory provided and creates the list of absolute paths filtering by extension"""
        abs_paths_lst = [
            join(root, name)
            for root, dirs, files in os.walk(r"./module/", topdown=True)
            for name in files
            if not extension or name.endswith(extension)
        ]

        self.files_list = [File(size=getsize(path), path=path) for path in abs_paths_lst]

    def get_sorting_preference(self):
        reverse_status = {1: True, 2: False}
        sort_option = int(input("Size sorting options:\n1. Descending\n2. Ascending\n"))
        if sort_option not in reverse_status:
            print("\nWrong option")
            return self.get_sorting_preference()
        self.sort_option = reverse_status[sort_option]

    def print_search_results(self):
        # filling out self.result_dict: dict
        for file in self.files_list:
            if file.size not in self.result_dict:
                self.result_dict[file.size] = [file.path]
            else:
                self.result_dict[file.size].append(file.path)

        self.result_dict = dict(sorted(self.result_dict.items(), reverse=self.sort_option))
        for size, path_list in self.result_dict.items():
            if path_list:
                print(f"{size} bytes\n{os.linesep.join(path_list)}")  # os.linesep is workaround to use '\n' in f string

    def check_for_duplicates(self):
        check = input("\nCheck for duplicates? (yes, no)\n").lower()
        if check == "yes":
            files_size_list = sorted((file.size for file in self.files_list), reverse=self.sort_option)
            sizes_with_several_files = [x for x in files_size_list if files_size_list.count(x) > 1]
            self.files_list = [file for file in self.files_list if file.size in sizes_with_several_files]
            
            # calculate hashes
            for file in self.files_list:
                file.get_hash()

    def print_duplicate_files(self):
        """this function prints the output(result) of the program. if a format key: \n values"""
        del_dict = {}
        self.result_dict = {}
        for f in self.files_list:
            if f.size not in self.result_dict:
                self.result_dict[f.size] = {f.hash: [f.path]}
            else:
                if f.hash not in self.result_dict[f.size]:
                    self.result_dict[f.size].update({f.hash: [f.path]})
                else:
                    if f.path not in self.result_dict[f.size][f.hash]:
                        self.result_dict[f.size][f.hash].append(f.path)

        size_hash_dictionary = dict(sorted(self.result_dict.items(), reverse=self.sort_option))

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
        decision = input("Delete files? (yes/no)")
        if decision.lower() not in {"yes", "no"}:
            print("Wrong option")
            return self.delete_files(dl_dict)

        elif decision.lower() == "yes":
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
        """this is the main function which calls other functions in a defined order"""
        self.get_files_list(input("Enter the file format or press 'return' for all:\n"))
        self.get_sorting_preference()
        self.print_search_results()
        self.check_for_duplicates()
        self.print_duplicate_files()


if __name__ == "__main__":
    if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
        exit(print("Directory is not specified"))

    handler = DuplicateFileHandler()
    handler.start()
