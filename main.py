import os
import pyautogui
import asyncio
import pyperclip
import sys
from getfiles import get_sorted_files_by_folder,check_dir_under_folder
from custom_print import DynamicTable
from processbar import process_bar

# Delay time in seconds

time_dale = 1.52

from datetime import datetime
from functools import wraps
headers = ["Sr.", "File Name", "Time"]
dynamic_table = DynamicTable(headers)
import os
from functools import wraps
from datetime import datetime

def timeit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()  # Record the start time
        result = await func(*args, **kwargs)  # Await the original function
        end_time = datetime.now()  # Record the end time
        elapsed_time = (end_time - start_time).total_seconds()  # Calculate elapsed time in seconds
        # Convert elapsed time to hours, minutes, and seconds
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        if 120 <= elapsed_time:
            formatted_time = f"{int(hours):02d}h:{int(minutes):02d}m:{int(seconds):02d}s"
        elif 60 <= elapsed_time:
            formatted_time = f"{int(minutes):02d}m:{int(seconds):02d}s"
        else:
            formatted_time = f"{elapsed_time}s"

        # Check the number of arguments to handle the dynamic_table addition
        if len(args) == 3:
            file_name = args[2]+'/'+os.path.basename(args[0])  # Get the file name
            dynamic_table.add_row([args[1], file_name, formatted_time])
        else:
            dynamic_table.add_row(['', '', ''])
            dynamic_table.add_row(['', "Total", formatted_time])

        # Log the function execution time
        # print(f"Function '{func.__name__}' took {formatted_time} to run.")
        
        return result  # Return the result of the original function

    return wrapper



# Step 4: Switch to the target application (e.g., Telegram)
async def switch_to_application():
    pyautogui.hotkey('win', '1')
    await asyncio.sleep(time_dale)
# Step 5: Send the file to Telegram with the file name as caption

@timeit
async def send_file_to_telegram(file_path,attempt=1,folderName=''):
    
    # Copy the file path to the clipboard
    pyperclip.copy(file_path)
    await asyncio.sleep(time_dale)
    # Switch to Telegram
    # await switch_to_application()
    # Simulate Ctrl + O to open the "Attach" dialog
    pyautogui.hotkey('ctrl', 'o')
    await asyncio.sleep(time_dale)
    # Paste the file path into the dialog
    pyautogui.hotkey('ctrl', 'v')
    await asyncio.sleep(time_dale)
    # Pres Enter to confirm the file selection
    pyautogui.press('enter')
    await asyncio.sleep(time_dale)
    # Copy the file name (without extension) as the caption
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    if folderName:
        file_name_without_extension = folderName+"_"+file_name_without_extension
    pyperclip.copy(file_name_without_extension)
    await asyncio.sleep(time_dale)
    # Paste the file name as the caption
    pyautogui.hotkey('ctrl', 'v')
    await asyncio.sleep(time_dale)
    # Press Enter to send the file with the caption
    pyautogui.press('enter')
    await asyncio.sleep(2)  # Give extra time to ensure the file is sent
    print(f'File "{file_path}" sent to Telegram.')
    # await switch_to_application()

# Main function to send files one by one to Telegram

async def print_all_paths(sorted_files_by_folder):
    """
    Print all file paths stored in the list of dictionaries.

    :param sorted_files_by_folder: List of dictionaries with folder names as keys and file paths as values.
    """
    # print(sorted_files_by_folder)
    if sorted_files_by_folder[-1]:
        for folder_data in sorted_files_by_folder[:-1]:
            for folder_name, files in folder_data.items():
                # print(f"\nFolder: {folder_name}")
                TotleFile = len(files)
                filenum = 1
                for file_path in files:
                    # print(file_path)
                    await send_file_to_telegram(file_path,str(filenum),folder_name)
                    print('Uploading Folder "',folder_name,'" % ','show : ')
                    process_bar(filenum,TotleFile )
                    await asyncio.sleep(time_dale)
                    filenum = filenum + 1
    else:
        folder_name = ''
        folder_data=sorted_files_by_folder[0]
        TotleFile = len(folder_data)
        filenum = 1
        for folder_name, files in folder_data.items():
                # print(f"\nFolder: {folder_name}")
                TotleFile = len(files)
                filenum = 1
                for file_path in files:
                    print(file_path)
                    await send_file_to_telegram(file_path,str(filenum),folder_name)
                    process_bar(filenum,TotleFile )
                    await asyncio.sleep(time_dale)
                    filenum = filenum + 1




@timeit
async def main():
    root_directory = sys.argv[1]  # Folder path
    print('Reading filss and folder')
    sorted_files_by_folder = get_sorted_files_by_folder(root_directory)
    sorted_files_by_folder.append(check_dir_under_folder(root_directory)[0])
    # Iterate over each file and send it one by one
    print("Uploading start .....")
    await switch_to_application()
    await print_all_paths(sorted_files_by_folder)
    await switch_to_application()



# Run the main function using asyncio
if __name__ == '__main__':
    asyncio.run(main())
