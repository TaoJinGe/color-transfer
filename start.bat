@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "VENV_PYTHON=%~dp0.venv\Scripts\python.exe"

if exist "%VENV_PYTHON%" goto check_dependencies
call :message find_python
where py >nul 2>nul
if not errorlevel 1 (
    py -3.11 --version >nul 2>nul
    if not errorlevel 1 set "PYTHON_COMMAND=py -3.11"
)
if not defined PYTHON_COMMAND (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON_COMMAND=python"
)
if not defined PYTHON_COMMAND goto python_error
%PYTHON_COMMAND% -c "import sys;raise SystemExit(sys.version_info[:2]!=(3,11))" >nul 2>nul
if errorlevel 1 goto python_error
call :message create_venv
%PYTHON_COMMAND% -m venv ".venv"
if errorlevel 1 goto venv_error

:check_dependencies
set "DEPENDENCY_MARKER=.venv\requirements-installed.txt"
if not exist "%DEPENDENCY_MARKER%" goto install_dependencies
fc /b "requirements.txt" "%DEPENDENCY_MARKER%" >nul 2>nul
if errorlevel 1 goto install_dependencies
goto launch

:install_dependencies
call :message install_dependencies
"%VENV_PYTHON%" -m pip install -r "requirements.txt"
if errorlevel 1 goto dependency_error
copy /y "requirements.txt" "%DEPENDENCY_MARKER%" >nul

:launch
if "%COLOR_TRANSFER_TEST_MODE%"=="1" (
    call :message check_success
    exit /b 0
)
call :message launching
"%VENV_PYTHON%" "app.py"
if errorlevel 1 goto launch_error
exit /b 0

:python_error
call :message python_error
goto failed
:venv_error
call :message venv_error
goto failed
:dependency_error
call :message dependency_error
goto failed
:launch_error
call :message launch_error
:failed
pause
exit /b 1

:message
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start_message.ps1" %1
exit /b 0
