@echo off
setlocal enabledelayedexpansion

echo [94m>> Checking Python installation...[0m
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3 and try again.
    exit /b 1
)

echo [94m>> Checking if virtual environment exists...[0m
if not exist .venv (
    echo [94m>> Creating virtual environment...[0m
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment. Please check your Python installation.
        exit /b 1
    )
)

echo [94m>> Activating virtual environment...[0m
call .venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment. Please check your Python installation.
    exit /b 1
)

echo [94m>> Installing dependencies...[0m
pip install -U pip
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies. Please check your network connection.
    exit /b 1
)

echo [94m>> Checking environment file...[0m
if not exist .env (
    if exist .env.example (
        echo [94m>> Creating .env file from .env.example...[0m
        copy .env.example .env
        echo Please edit the .env file to add your OpenAI API key before running the application.
        echo Press Enter to continue or Ctrl+C to exit and edit the file now.
        pause
    )
)

echo [94m>> Creating necessary directories...[0m
if not exist logs\history mkdir logs\history

echo [94m>> Starting the application...[0m
streamlit run src\app\Home.py

endlocal 