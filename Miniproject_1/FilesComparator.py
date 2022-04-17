"""
Author: Said Khudoyan
Description: A simple program, that lets you check, if two folders have different files (ignoring their extension)
If the two folders have indeed different files, those will be moved to a target folder, which the user should choose.

To be on the safe side, the different files in the old folders won't be removed, but it can be easily implemented.
"""

import os
import shutil
import time
from tkinter import filedialog, messagebox
from tkinter.messagebox import askyesno


def checker(dir_1, dir_2):
    # Get images or files
    files_1 = os.listdir(dir_1)
    files_2 = os.listdir(dir_2)
    # Remove extensions of files
    files_1_new = [os.path.splitext(file)[0] for file in files_1]
    files_2_new = [os.path.splitext(file)[0] for file in files_2]
    # Check if elements of files_1_new in files_2_new and the other way around
    diffs_1 = [element for element in files_1_new if element not in files_2_new]
    diffs_2 = [element for element in files_2_new if element not in files_1_new]
    # Now that we know which files are different, we get their extensions back
    matches = [filename for filename in set(files_1 + files_2) if os.path.splitext(filename)[0] in diffs_1]
    matches_2 = [filename for filename in set(files_1 + files_2) if os.path.splitext(filename)[0] in diffs_2]
    # Finally, we get the path of the different files and return them
    some_path = [os.path.join(dir_1, file) for file in matches]
    some_path_2 = [os.path.join(dir_2, file) for file in matches_2]
    combi = some_path + some_path_2
    return matches, matches_2, combi


# Select the two folders you want to compare
path_1 = filedialog.askdirectory()
# Add some time delay when asking for folder
time.sleep(0.5)
path_2 = filedialog.askdirectory()
# Result of different files we get, when comparing both folders
f1, f2, combined_path = checker(path_1, path_2)
yes_no = askyesno("Please choose", "Do you want to see the differences?")
if yes_no:
    messagebox.showinfo("Different files", f"The different files are: \n"
                                           f"====================\n"
                                           f"{f1+f2}\n"
                                           f"====================\n")
answer = askyesno("Please choose", "Do you want to move the different files to another folder?")
if answer:
    ans = askyesno("Please choose", "Are you sure about this?")
    if ans:
        messagebox.showinfo("Moving_Process", "\nClick OK to choose Target Folder\n")
        # Ask for target directory
        dir_3 = filedialog.askdirectory()
        directory = "DifferentFiles"  # Target directory name (can be changed)
        path = os.path.join(dir_3, directory)
        # If target folder does not exist, copy files to target folder, else stop process
        if not os.path.exists(path):
            os.makedirs(path)
            for file_path in combined_path:
                shutil.copy2(file_path, path)
            messagebox.showinfo("Moving_Process", "\n====End of moving====\n")
        else:
            messagebox.showinfo("Already exists", "The folder already exists, moving process stopped!")
