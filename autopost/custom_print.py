import pandas as pd
import os
import random
from colorama import Fore, Style, init
import time
from functools import wraps
# Initialize colorama
init(autoreset=True)

def save_to_file_decorator(file_name):
    """Decorator to save table data to a file after adding a row."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, row, *args, **kwargs):
            # Call the original add_row method
            result = func(self, row, *args, **kwargs)
            if row[0] == '':
                self.save_table_to_file(file_name)
                # Save the current table data to a file
            return result
        return wrapper
    return decorator



class DynamicTable:
    def __init__(self, headers,colorfull=True):
        self.headers = headers
        self.data = []
        if colorfull:
            self.colors = [Fore.WHITE,Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA]
            self.used_colors = [Fore.WHITE,Fore.RED,Fore.MAGENTA,Fore.BLUE,]
        else:
            self.colors = [Fore.WHITE]
            self.used_colors = [Fore.WHITE]  # To keep track of used colors
        

    @save_to_file_decorator("table_data.txt")
    def add_row(self, row):
        # Add a new row to the data
        self.data.append(row)
        # Refresh the table display
        self.refresh_table()

    def save_table_to_file(self, file_name):
        """Save the current table data to a text file."""
        # Create a DataFrame from the data
        df = pd.DataFrame(self.data, columns=self.headers)
        # Save the DataFrame to a text file
        with open(file_name, "w") as f:
            f.write(df.to_markdown(index=False, tablefmt="grid"))

    def refresh_table(self):
        # Clear the console screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # Create a DataFrame from the data
        df = pd.DataFrame(self.data, columns=self.headers)
        
        # Set display options to automatically adjust column width
        pd.set_option('display.max_colwidth', None)  # No limit on column width
        pd.set_option('display.width', None)  # Automatically adjusts to content
        pd.set_option('display.colheader_justify', 'center')  # Center align column headers
        
        # Display the DataFrame as a table with borders
        table_str = df.to_markdown(index=False, tablefmt="grid")
        
        # Add colors for the table display
        colored_table_str = self.apply_color_to_table(table_str)
        
        # Print the formatted table
        print("\n" + colored_table_str + "\n")

    def apply_color_to_table(self, table_str):
        # Split the table into lines
        lines = table_str.split("\n")
        colored_lines = []

        # Apply unique color to each line
        for line in lines:
            if len(self.used_colors) == len(self.colors):  # Reset if all colors are used
                self.used_colors = []
            # Pick a color that hasn't been used yet
            available_colors = [color for color in self.colors if color not in self.used_colors]
            color = random.choice(available_colors)
            colored_lines.append(color + line + Style.RESET_ALL)
            self.used_colors.append(color)  # Mark this color as used

        # Join the colored lines back together
        return "\n".join(colored_lines)


if __name__ == "__main__":

    headers = ["Sr.", "File Name", "Time"]
    dynamic_table = DynamicTable(headers)


    dynamic_table.add_row(["1", "ShortName.mp4", "2.0001s"])
    time.sleep(1)
    dynamic_table.add_row(["2", "VeryLongFileNameThatExceedsNormalLength.mp4", "1.8002s"])
    time.sleep(1)
    dynamic_table.add_row(["3", "MediumLengthFileName.mp4", "3.1234s"])