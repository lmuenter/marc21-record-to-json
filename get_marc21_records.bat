@echo off
rem Changing to script location
cd %~dp0

if not exist ".\venv" (
    echo Setting up virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

echo Activating virtual environment...
call .\venv\Scripts\activate

call :are_requirements_satisfied
if not %ERRORLEVEL% equ 0 (
    echo Found Missing dependencies. Installing dependencies...
    pip install -r requirements.txt
)

echo Parsing MARC21XML data...
python get_marc21_records.py %*

echo Deactivating virtual environment...
call .\venv\Scripts\deactivate

exit /b

:are_requirements_satisfied
for /f "delims==" %%i in (requirements.txt) do (
    for /f "tokens=1" %%j in ("%%i") do (
        pip show %%j >nul 2>&1
        if not %ERRORLEVEL% equ 0 (
            exit /b 1
        )
    )
)
goto :eof
