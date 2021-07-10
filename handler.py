# write your code here
import os
import sys

args = sys.argv

if len(args) < 2:  # 2 here because counting starts from 0, and args[0] is the name of a python3 script
    print("Directory is not specified")
else:
    #print(args)
    folder = args[1]
    for root, dirs, files in os.walk(folder, topdown=True):
        for name in files:
            print(os.path.join(root, name))
