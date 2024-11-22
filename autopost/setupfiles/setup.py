import sys
import subprocess


def print_config_file():
    print()
    print("#"*25,' config.py Start ',"#"*25,'\n')
    print(read_text_file('config.py'))
    print()
    print("#"*25,' config.py End ',"#"*25,'\n')
    print("Commond is autopost set <key> <value>\n")
    print('Exmalpe:\n\n\tkey = time_dale\n\tvalue = 1.0')


def find_line_number(filename, search_key):
    """Finds and returns the line numbers where `search_key` appears in the file. 
    If not found, returns the line number after the last line."""
    line_numbers = []
    # print(search_key)
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if search_key in line:
                    line_numbers.append(line_number)
        
        # If search_key was found, return the list of line numbers
        if line_numbers:
            return line_numbers
        else:
            # If not found, return the next line number after the last line
            return False
    except FileNotFoundError:
        return f"The file {filename} was not found."


def delete_line_by_number(filename, line_number):
    """Deletes the line at the specified line number in the file."""
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        
        # Check if the given line number is valid
        if 1 <= line_number <= len(lines):
            # Remove the specified line (adjust for 0-based index)
            del lines[line_number - 1]
            
            # Write the modified content back to the file
            with open(filename, "w") as file:
                file.writelines(lines)
            
            # print(f"Line {line_number} has been deleted from {filename}.")
        else:
            pass
            # print(f"Line {line_number} is out of range. The file has only {len(lines)} lines.")
            
    except FileNotFoundError:
        print(f"The file {filename} was not found.")


def insert_line_at_number(filename, line_number, new_data):
    """Inserts `new_data` at the specified line number in the file."""
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        
        # Adjust line_number for 1-based indexing
        if line_number <= 0:
            print("Line number should be greater than 0.")
            return

        # Insert the new line at the specified position
        if line_number <= len(lines):
            lines.insert(line_number - 1, new_data + "\n")
        else:
            # If line_number is beyond the end of the file, append the new data
            lines.append(new_data + "\n")
        
        # Write the updated lines back to the file
        with open(filename, "w") as file:
            file.writelines(lines)
        
        # print(f"Inserted data at line {line_number} in {filename}.")
    except FileNotFoundError:
        print(f"The file {filename} was not found.")



def Set_All_Config(key, value):
    filename = "config.py"
    line_numbers = find_line_number(filename,key)
    if  line_numbers == False :
        print (key," Not Requrment " )
        print_config_file()
    else:
        # If the search_key was not found, line_numbers will have the next available line number
        line_number = line_numbers[-1]
        # print(f"Line number to insert: {line_number}")
        try:
            # If line_number is not in range or invalid, avoid deletion attempt
            delete_line_by_number(filename, line_number)
        except Exception as e:
            print(f"Error in deletion: {e}")

        # Insert the new data at the specified line number
        try:
            value = float(value)
            insert_line_at_number(filename, line_number, f"{key} = {value}")
        except:
            value = str(value)
            insert_line_at_number(filename, line_number, f"{key} = '{value}'")
        print_config_file()


def run_other_file(file_path, args):
    """
    Run another Python file directly within the current script.

    Parameters:
    - file_path (str): The path to the Python file to be run.
    - args (list): Additional arguments to pass to the file.
    """
    try:
        # Prepare the arguments
        sys.argv = [file_path] + args

        # Read and execute the code from the file
        with open(file_path, "r") as file:
            code = file.read()
            exec(code, globals())

    except Exception as e:
        # Handle any errors that occur during execution
        print(f"Error running the file: {e}")

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

