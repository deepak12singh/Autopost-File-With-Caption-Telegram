
import sys
import logging
from setupfiles.help import show_detailed_help, show_command_help
from setupfiles.setup import  Set_All_Config,read_text_file,print_config_file
import subprocess

# Setting up logging configuration
logging.basicConfig(
    filename='application.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log starting point

def main():
    # Check if there are enough command-line arguments
    if len(sys.argv) < 3:
        logging.error("Insufficient arguments provided.")
        print("\n   Error: Insufficient arguments provided. Use 'autopost help' for usage information.\n")
        return

    # Retrieve command-line arguments
    argv = sys.argv
    command = argv[1].lower()

    logging.info("Command received: %s", command)

    # Process based on command
    if command == 'run':
        if argv[2] == 'here':
            current_path = argv[-1]
            # print(f"     Current path: {current_path}    ")
            logging.info("Current path set to: %s", current_path)
            # Run the setting.py first
            subprocess.run([r'C:\PythonCostumScript\autopost\.venv\Scripts\python.exe', r'setting.py','run','here',  current_path])
            # Now run main.py after setting.py completes

        elif argv[2] in ('path', 'p'):
            if len(argv) > 3:
                specified_path = argv[3]
                print(f"     Path: {specified_path}     ")
                logging.info("Path set to: %s", specified_path)
                # Now run main.py with the specified path
                subprocess.run([r'C:\PythonCostumScript\autopost\.venv\Scripts\python.exe', r'setting.py','run','path',  specified_path])
            else:
                logging.error("Path argument missing for command 'path' or 'p'")
                print("Error: Path argument is missing. Please specify a path after 'path' or 'p' command.")
        else:
            show_command_help('run')
            
        
    elif command in ('help', 'h', '-h'):
        if len(argv) > 3:
            print('.................',argv[2])
            value = argv[2]
            show_command_help(value)
        else:
            show_detailed_help()
    elif command in ('set', '-s'):
        argv = argv[:-1]
        if len(argv) > 2:
            key = argv[2]
            if key == '-h':
                print_config_file()
            else:
                try:
                    value = argv[3]
                    Set_All_Config(key, value)
                except :
                    print_config_file()
                    
        else:
            logging.error("Path argument missing for command 'set' or '-s'")
            print("Error: key argument is missing. Please specify a key after 'key' and 'value' of it command.")
            print_config_file()
    else:
        logging.info("Displaying detailed help.")
        command_setting = [r'C:\PythonCostumScript\autopost\.venv\Scripts\python.exe', r'setting.py']
        for i in argv:
            command_setting.append(i)
        subprocess.run(command_setting)

if __name__ == '__main__':
    main()
    logging.info("Script ended")

    


    