import os
import re
from pathlib import Path
import asyncio

def natural_sort_key(filename):
    """
    Generate a sorting key that allows for natural sorting of filenames.
    
    :param filename: The filename to generate the sorting key for.
    :return: A list that can be used as a key for sorting.
    """
    # Split the filename into a list of numbers and strings
    return [int(part) if part.isdigit() else part.lower() for part in re.split('(\d+)', filename)]

def get_sorted_folders(directory):
    """
    Get a list of sorted folders in the specified directory.

    :param directory: The directory path to check for subfolders.
    :return: A sorted list of folder paths.
    """
    path = Path(directory)
    folders = [folder for folder in path.iterdir() if folder.is_dir()]

    # Sort folders using the natural sort key
    return sorted(folders, key=lambda f: natural_sort_key(f.name))

def list_sorted_files_in_folder(folder_path):
    """
    List all files in a given folder, sorted using a natural sort.

    :param folder_path: The path of the folder to list files from.
    :return: A sorted list of file paths.
    """
    files_list = []

    # Loop through the folder and list all files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)

    # Sort files using the natural sort key
    return sorted(files_list, key=lambda f: natural_sort_key(os.path.basename(f)))

def get_sorted_files_by_folder(directory):
    """
    Get a sorted list of folders and the sorted files within each folder.

    :param directory: The root directory to start from.
    :return: A list of dictionaries where each dictionary represents a folder and its sorted files.
    """
    # Step 1: Get a sorted list of folders in the root directory
    sorted_folders = get_sorted_folders(directory)
    return_data = []

    # Step 2: Iterate through each sorted folder, list sorted files, and collect results
    if sorted_folders:
        for folder in sorted_folders:
            # List and sort files within the current folder
            sorted_files = list_sorted_files_in_folder(folder)

            # Create a dictionary entry for the current folder
            folder_data = {folder.name: sorted_files}
            return_data.append(folder_data)
    else:
        # If there are no subfolders, process the root directory itself
        folder_name = os.path.basename(directory)
        sorted_files = list_sorted_files_in_folder(directory)

        # Create a dictionary entry for the root directory
        folder_data = {folder_name: sorted_files}
        return_data.append(folder_data)

    return return_data

def check_dir_under_folder(directory):
    """
    Checks for subdirectories in the given directory and returns a sorted list of folder paths.

    :param directory: The directory path to check for subfolders.
    :return: A tuple indicating if folders exist, a sorted list of folder paths, and folder names.
    """
    path = Path(directory)
    folders = [folder.name for folder in path.iterdir() if folder.is_dir()]
    folders_list = [os.path.join(directory, i) for i in folders]

    if folders:
        # Sort the list of folders using the natural sort key
        folders_list_sorted = sorted(folders_list, key=lambda f: natural_sort_key(os.path.basename(f)))
        folders_sorted = sorted(folders, key=natural_sort_key)
        return True, folders_list_sorted, folders_sorted
    else:
        return False, [directory], []

async def process_folders(sorted_files_by_folder):
    """
    Process folders and list files.

    :param sorted_files_by_folder: List of dictionaries with folder names and sorted files.
    """
    for folder_data in sorted_files_by_folder:
        for folder_name, root_files in folder_data.items():
            # Ensure root_files is a list of files (not a boolean)
            if isinstance(root_files, list):
                for file_path in root_files:
                    print(f"Processing file: {file_path}")
            else:
                print(f"Error: Expected a list of files, but got {type(root_files)} instead.")

def print_all_paths(sorted_files_by_folder):
    """
    Print all file paths stored in the list of dictionaries.

    :param sorted_files_by_folder: List of dictionaries with folder names as keys and file paths as values.
    """
    print(sorted_files_by_folder[-1])
    for folder_data in sorted_files_by_folder[:-1]:
        for folder_name, files in folder_data.items():
            print(f"\nFolder: {folder_name}")
            for file_path in files:
                print(file_path)

if __name__ == "__main__":
    # Specify the directory you want to start from
    root_directory = r"C:\Users\Sachin_Singh\Desktop\New folder\New folder\New folder\Test\Day1"  # Change this to your directory path

    # Get the sorted files organized by folders
    sorted_files_by_folder = get_sorted_files_by_folder(root_directory)
    
    # Check if there are subfolders and handle them accordingly
    folder_exists, folders_list, folder_names = check_dir_under_folder(root_directory)

    if folder_exists:
        # Process the folders
        for folder in folders_list:
            sorted_files = list_sorted_files_in_folder(folder)
            sorted_files_by_folder.append({os.path.basename(folder): sorted_files})
    else:
        # Process the root directory
        sorted_files = list_sorted_files_in_folder(root_directory)
        sorted_files_by_folder.append({os.path.basename(root_directory): sorted_files})

    # Print the collected return data
    print("\nReturn Data:")
    print(sorted_files_by_folder)

    # Print all paths of files and folders
    asyncio.run(process_folders(sorted_files_by_folder))
