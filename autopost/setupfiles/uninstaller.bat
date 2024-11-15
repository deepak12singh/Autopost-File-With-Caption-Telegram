@echo off

REM Define the project name and paths
set "project_name=autopost"
set "PROJECT_PATH=C:\PythonCostumScript\%project_name%"

:: Check for administrator privileges
net session >nul 2>&1
if errorlevel 1 (
    echo [Error] Administrator privileges are required to uninstall.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Run Python script to remove path registration
echo Removing registered paths...
python "%PROJECT_PATH%\setupfiles\remove_path.py" "%PROJECT_PATH%"
if errorlevel 1 (
    echo [Error] Failed to unregister paths.
    exit /b 1
)

:: Remove the project folder
if exist "%PROJECT_PATH%" (
    echo Deleting project folder at %PROJECT_PATH%...
    rmdir /S /Q "%PROJECT_PATH%"
    if errorlevel 1 (
        echo [Error] Failed to delete the project folder.
        exit /b 1
    )
    echo Project folder deleted successfully.
) else (
    echo [Warning] Project folder not found at %PROJECT_PATH%.
)

:: Notify completion

exit /b 0


