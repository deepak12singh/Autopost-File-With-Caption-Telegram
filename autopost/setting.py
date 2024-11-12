
import sys
import subprocess
from setupfiles.help import show_detailed_help
print("running the setting file ")
def main():
    # Check if there are enough command-line arguments
    argv = sys.argv
    # Get the command-line argument (the path in this case)
    command = sys.argv[1].lower()
    if command == 'run':
        if argv[2] in ('path', 'here'):
            # Get the current path
            current_path = sys.argv[3]
            print(f"Setting current path to: {current_path}")
            # After setting up, now call main.py with the correct argument
            try:
                subprocess.run([r'C:\autopost\.venv\Scripts\python.exe', r'main.py', current_path])
            except Exception as e:
                print(f"Error executing main.py: {str(e)}")
    else:
        show_detailed_help()



if __name__ == '__main__':
    main()

    
    