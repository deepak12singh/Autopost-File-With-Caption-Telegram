
print("Running the Run.py ..................")
import sys
import logging
from setupfiles.help import show_detailed_help, show_command_help
from config import GENERATIVE_AI_KEY
from setupfiles.setup import Set_GENERATIVE_AI_KEY_, Set_All_Config,read_text_file
import subprocess

# Setting up logging configuration
logging.basicConfig(
    filename='application.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log starting point
logging.info("Script started")
logging.info("Config file data: GENERATIVE_AI_KEY=%s", GENERATIVE_AI_KEY)

def main():
    # Check if there are enough command-line arguments
    if len(sys.argv) < 3:
        logging.error("Insufficient arguments provided.")
        print("Error: Insufficient arguments provided. Use 'autodata help' for usage information.")
        return

    # Retrieve command-line arguments
    argv = sys.argv
    command = argv[1].lower()

    logging.info("Command received: %s", command)

    # Process based on command
    if command == 'run':
        if argv[2] == 'here':
            current_path = argv[-1]
            print(f"     Current path: {current_path}    ")
            logging.info("Current path set to: %s", current_path)
            # Run the setting.py first
            subprocess.run([r'C:\autopost\.venv\Scripts\python.exe', r'setting.py','run','here',  current_path])
            # Now run main.py after setting.py completes

        elif argv[2] in ('path', 'p'):
            if len(argv) > 3:
                specified_path = argv[3]
                print(f"     Path: {specified_path}     ")
                logging.info("Path set to: %s", specified_path)
                # Now run main.py with the specified path
                subprocess.run([r'C:\autopost\.venv\Scripts\python.exe', r'setting.py','run','path',  specified_path])
            else:
                logging.error("Path argument missing for command 'path' or 'p'")
                print("Error: Path argument is missing. Please specify a path after 'path' or 'p' command.")
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
            if key == 'key':
                value = argv[3]
                print(f"     Path: {key}  = {value}   ")
                Set_GENERATIVE_AI_KEY_(value)
            elif key == '-h':
                print(read_text_file('config.py'))
            else:
                value = argv[3]
                Set_All_Config(key, value)
        else:
            logging.error("Path argument missing for command 'set' or '-s'")
            print("Error: key argument is missing. Please specify a key after 'key' and 'value' of it command.")
    else:
        logging.info("Displaying detailed help.")
        command_setting = [r'C:\autopost\.venv\Scripts\python.exe', r'setting.py']
        for i in argv:
            command_setting.append(i)
        subprocess.run(command_setting)

if __name__ == '__main__':
    main()
    logging.info("Script ended")

    


    