@echo off
:: Store the current directory
set "CURRENT_DIR=%CD%"

:: Set the project directory path
set "PROJECT_DIR=C:\autopost"

:: Change directory to the project folder
cd /d "%PROJECT_DIR%"
if errorlevel 1 (
    echo Failed to change directory to %PROJECT_DIR%
    pause
    exit /b 1
)

:: Check if the virtual environment folder exists
if not exist ".\.venv\Scripts\activate" (
    echo Virtual environment not found at .\.venv.
    pause
    exit /b 1
)

:: Activate the virtual environment
call .\.venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate the virtual environment.
    pause
    exit /b 1
)

:: Verify if Python is available in the virtual environment
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not found in the virtual environment.
    pause
    exit /b 1
)

:: Handle the 'here' or 'set' command
if "%~1"=="run" (
    :: Run the Python script with CURRENT_DIR as an argument
    python run.py %* "%CURRENT_DIR%"
    if errorlevel 1 (
        echo Failed to run run.py.
        pause
    )
) else (
    python run.py %* "%CURRENT_DIR%"
    if errorlevel 1 (
        echo Failed to run help.py.
        
    )
)

:: Deactivate the virtual environment
call deactivate
if errorlevel 1 (
    echo Failed to deactivate the virtual environment.
    pause
)

:: Return to the original directory
cd /d "%CURRENT_DIR%"

:: Final message
::echo Script completed successfully.
::pause
