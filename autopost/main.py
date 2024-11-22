import os
import pyautogui
import asyncio
import pyperclip
import sys
from getfiles import get_sorted_files_by_folder, check_dir_under_folder
from custom_print import DynamicTable
from processbar import process_bar
from datetime import datetime
from functools import wraps
from config import *



# Setup dynamic table headers
headers = ["Sr.", "File Name", "Time"]
dynamic_table = DynamicTable(headers,colorfull=colorfull)

def timeit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = await func(*args, **kwargs)
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()

        # Format elapsed time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = (
            f"{int(hours):02d}h:{int(minutes):02d}m:{int(seconds):02d}s"
            if elapsed_time >= 120 else
            f"{int(minutes):02d}m:{int(seconds):02d}s"
            if elapsed_time >= 60 else
            f"{elapsed_time:.2f}s"
        )

        # Add row to dynamic table
        if len(args) >= 2:
            folder_name = args[2] if len(args) > 2 else ''
            file_name = folder_name + '/' + os.path.basename(args[0]) if folder_name else os.path.basename(args[0])
            dynamic_table.add_row([args[1], file_name, formatted_time])
        else:
            dynamic_table.add_row(['', '', ''])
            dynamic_table.add_row(['', "Total", formatted_time])

        return result

    return wrapper

async def switch_to_application():
    """Switch to Telegram application."""
    pyautogui.hotkey('win', '1')
    await asyncio.sleep(time_dale)

@timeit
async def send_file_to_telegram(file_path, attempt=1, folder_name=''):
    """Send a file to Telegram."""

    pyperclip.copy(file_path)
    await asyncio.sleep(time_dale)
    pyautogui.hotkey('ctrl', 'o')
    await asyncio.sleep(time_dale)
    pyautogui.hotkey('ctrl', 'v')
    await asyncio.sleep(time_dale)
    pyautogui.press('enter')
    await asyncio.sleep(time_dale)

    # Only add the folder name as a prefix if the file is under a folder
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    if folder_name:
        file_name_without_extension = folder_name + folder_and_file_join_symblo + file_name_without_extension
    pyperclip.copy(file_name_without_extension)
    await asyncio.sleep(time_dale)
    pyautogui.hotkey('ctrl', 'v')
    await asyncio.sleep(time_dale)
    pyautogui.press('enter')
    await asyncio.sleep(2)
    print(f'File "{file_path}" sent to Telegram.')

async def process_folders(sorted_files_by_folder,totle_file=0):
    """Process all folders and send files to Telegram."""
    File_number = 0
    for folder_data in sorted_files_by_folder[:-1]:
        for folder_name, files in folder_data.items():
            total_files = len(files)
            for index, file_path in enumerate(files, start=1):
                if folder_name == "Nothing_Folder_Name":
                    await send_file_to_telegram(file_path, str(index))
                    process_bar(index, total_files,symbol='*',bar_length=100,folder_name='All File Status')
                else:
                    await send_file_to_telegram(file_path, str(index), folder_name)
                    process_bar(index, total_files,folder_name=folder_name)
                    File_number = File_number + 1
                    print('')
                    process_bar(File_number,totle_file,symbol='*',bar_length=100,folder_name='All File Status')
                await asyncio.sleep(time_dale)


@timeit
async def main():
    """Main function to send files to Telegram."""
    root_directory = sys.argv[1]
    print('Reading files and folders...')
    sorted_files_by_folder = get_sorted_files_by_folder(root_directory)
    # Only append the sorted folder paths (not the boolean result)
    folder_exists, folders_list, _ = check_dir_under_folder(root_directory)
    
    total_files = 0
    for i, folder_dict in enumerate(sorted_files_by_folder):
        if isinstance(folder_dict, dict):  # Ensure it's a dictionary
            for key, value in folder_dict.items():
                total_files += len(value)  # Increment total_files by the length of the list
        # Append `folders_list` to `sorted_files_by_folder`
    if folder_exists:
        sorted_files_by_folder.append(folders_list)
    else:
        dirc = sorted_files_by_folder[0]
        for key in list(dirc.keys()):
            data = dirc[key]
            dirc.pop(key)
            dirc["Nothing_Folder_Name"]=data
        # sorted_files_by_folder[0] = dirc
        sorted_files_by_folder.append([])
    print("Uploading started...")
    await switch_to_application()
    await process_folders(sorted_files_by_folder,totle_file=total_files)
    await switch_to_application()

if __name__ == '__main__':
    asyncio.run(main())
