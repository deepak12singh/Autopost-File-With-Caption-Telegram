import os
import sys
import winreg

def remove_from_system_path(path_to_remove):
    # Normalize the path for consistent matching
    path_to_remove = os.path.normpath(path_to_remove)
    
    # Access the user's PATH environment variable in the Windows registry
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            # Retrieve the PATH value from the registry
            path_env, _ = winreg.QueryValueEx(key, "Path")
            
            # Split the PATH by the system path separator
            path_elements = path_env.split(os.pathsep)
            
            # Check if the path is in PATH
            if path_to_remove in map(os.path.normpath, path_elements):
                # Remove the path if it exists in the PATH variable
                path_elements = [p for p in path_elements if os.path.normpath(p) != path_to_remove]
                
                # Rejoin the remaining paths and update the PATH environment variable in the registry
                new_path_env = os.pathsep.join(path_elements)
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_env)
                
                print(f"Permanently removed '{path_to_remove}' from PATH.")
            else:
                print(f"The path '{path_to_remove}' is not in the PATH environment variable.")
            
            # Display the updated PATH
            # print(f"New PATH:\n{new_path_env}")
    except FileNotFoundError:
        print("Could not find the PATH variable in the registry.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path_to_remove = sys.argv[1]
        remove_from_system_path(path_to_remove)
    else:
        print("Please provide the path to remove as an argument.")
