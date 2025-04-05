#!/bin/bash

# Print colorful messages
print_message() {
    echo -e "\e[1;34m>> $1\e[0m"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_message "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
print_message "Activating virtual environment..."
source .venv/bin/activate

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Failed to activate virtual environment. Please check your Python installation."
    exit 1
fi

# Install dependencies
print_message "Installing dependencies..."
pip install -U pip
pip install -r requirements.txt

# Check if .env file exists, create from example if it doesn't
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    print_message "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit the .env file to add your OpenAI API key before running the application."
    echo "Press Enter to continue or Ctrl+C to exit and edit the file now."
    read
fi

# Create necessary directories
print_message "Creating necessary directories..."
mkdir -p logs/history

# Run the application
print_message "Starting the application..."
streamlit run src/app/Home.py 