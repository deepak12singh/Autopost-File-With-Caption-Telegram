import sys
from .setup import read_text_file

def show_intro_help():
    """Display introductory help message."""
    print("=" * 50)
    print(" Welcome to the  Automation  Videos and Image File Post Tool!")
    print("=" * 50)
    print("\nThis tool automates various data-related tasks, including running scripts, setting keys, and more.")
    print("\nUse the commands below to navigate the tool or get help on specific features.")
    print("=" * 50)


def show_detailed_help():
    """Display a more detailed help message with categories."""
    print(read_text_file(r'.\setupfiles\helptxtfile\help.txt'))


def show_command_help(command):
    """Show help for a specific command."""
    if command == 'run':
        print(read_text_file(r'.\setupfiles\helptxtfile\run.txt'))
        
    elif command == 'key':
        print(read_text_file(r'.\setupfiles\helptxtfile\key.txt'))
    
    elif command == 'set':
        print(read_text_file(r'.\setupfiles\helptxtfile\key.txt'))
    
    else:
        print("\nInvalid command! Type 'ProjectStart help' for general help.")
        print("Try 'ProjectStart -h <command>' for more specific help on a particular command.")


def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) == 1:
        show_intro_help()  # Show the intro help
    elif len(sys.argv) == 2 and sys.argv[1] == "help":
        show_detailed_help()  # Show detailed help
    elif len(sys.argv) == 3 and sys.argv[1] == "-h":
        show_command_help(sys.argv[2])  # Show help for a specific command
    else:
        show_detailed_help()


if __name__ == "__main__":
    main()
