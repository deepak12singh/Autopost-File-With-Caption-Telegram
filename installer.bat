@echo off
:: ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:: Batch Script for Uninstallation                              +
:: Author: Deepak Singh                                         +
:: Description: Removes the project folder and cleans up paths. +
:: ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
REM Define project name and paths
set "project_name=autopost"
set SOURCE=%~dp0%project_name%
set DEST=C:\PythonCostumScript\%project_name%
set SCRIPT_DIR=%~dp0installer\
set SCRIPT_DIR_BAT=%~dp0


REM Check for administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Step 1: Copy the project folder to C:\
echo Copying project folder to %DEST%...
xcopy /E /I /Y "%SOURCE%" "%DEST%"
if %errorlevel% neq 0 (
    echo Error: Failed to copy project folder. Exiting...
    exit /b
)

REM Step 2: Set environment path variable
if exist "%SCRIPT_DIR%\set_autodata_path.py" (
    echo Adding %DEST% to PATH in registry and current session...
    python "%SCRIPT_DIR%\set_autodata_path.py" "%SCRIPT_DIR_BAT%"
    if %errorlevel% neq 0 (
        echo Error: Failed to set PATH. Please check set_autodata_path.py.
        exit /b
    )
) else (
    echo Warning: set_autodata_path.py not found in %SCRIPT_DIR%. Skipping PATH setup.
)

REM Step 3: Change directory to the project folder
cd /d %DEST%

REM Step 4: Create a virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error: Virtual environment creation failed.
        exit /b
    )
) else (
    echo Virtual environment already exists.
)

REM Step 5: Activate the virtual environment and install requirements
set VENV_PATH="%DEST%\.venv\Scripts\activate.bat"
if exist %VENV_PATH% (
    echo Activating virtual environment...
    call %VENV_PATH%
    python.exe -m pip install --upgrade pip
    if exist "requirements.txt" (
        echo Installing requirements from requirements.txt...
        pip install -r "requirements.txt"
    ) else (
        echo Warning: requirements.txt not found in %DEST%.
    )
) else (
    echo Error: Activation script not found. Check if .venv was created successfully.
    exit /b
)

echo Installation complete.
pause
cd /d "%CURRENT_DIR%"