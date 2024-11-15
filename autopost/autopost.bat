@echo off
:: ----------------------------------------------------
:: Batch Script to Manage Python Project
:: Author: Deepak Singh
:: Description: Automates setup, activation, running,
::              and uninstallation of a Python project.
:: -----------------------------------------------------

:: Store the current directory
set "CURRENT_DIR=%CD%"

:: Set the project directory path
set "PROJECT_DIR=C:\PythonCostumScript\autopost"

:: Change directory to the project folder
cd /d "%PROJECT_DIR%"
if errorlevel 1 (
    echo [Error] Failed to change directory to %PROJECT_DIR%.
    pause
    cd /d "%CURRENT_DIR%"
    exit /b 1
)

:: Handle 'uninstall' command
if "%~1"=="uninstall" (
    echo Starting uninstallation process...
    call "%PROJECT_DIR%\setupfiles\uninstaller.bat"
    if errorlevel 1 (
        echo [Error] Uninstallation process failed.
        pause
        cd /d "%CURRENT_DIR%"
        exit /b 1
    )
    echo.
    echo.                             ... Thanks for using %project_name%, nice to meet you ...
    echo.                                                                                                   
    echo.                                        Uninstallation complete.
    echo.
    echo.
    cd /d "%CURRENT_DIR%"
    exit /b 0
)

:: Check if the virtual environment folder exists
if not exist ".\.venv\Scripts\activate" (
    echo [Error] Virtual environment not found at .\.venv.
    pause
    cd /d "%CURRENT_DIR%"
    exit /b 1
)

:: Activate the virtual environment
call .\.venv\Scripts\activate
if errorlevel 1 (
    echo [Error] Failed to activate the virtual environment.
    pause
    cd /d "%CURRENT_DIR%"
    exit /b 1
)

:: Verify if Python is available in the virtual environment
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python is not found in the virtual environment.
    pause
    cd /d "%CURRENT_DIR%"
    exit /b 1
)

:: Handle 'run' or default command
if "%~1"=="run" (
    :: echo Running the main script...
    python run.py %* "%CURRENT_DIR%"
    if errorlevel 1 (
        echo [Error] Failed to execute run.py.
        pause
    )
) else (
    :: echo Running the default script...
    python run.py %* "%CURRENT_DIR%"
    if errorlevel 1 (
        echo [Error] Failed to execute run.py.
        pause
    )
)

:: Deactivate the virtual environment
call deactivate
if errorlevel 1 (
    echo [Warning] Failed to deactivate the virtual environment.
    pause
)

:: Return to the original directory
cd /d "%CURRENT_DIR%"
:: echo Script completed successfully.
exit /b 0
