#!/bin/sh

REPOSITORY_LINK=https://github.com/vasilypht/crypto-methods.git 
INSTALLATION_PATH=$HOME/crypto-methods
REQUIREMENTS_FILE="requirements.txt"


command_exists() {
    command -v $* >/dev/null
}


# Checking if git is installed
command_exists git || {
    echo "git is not installed!"
    echo "Install git and try again..."
    exit 1
}

git clone $REPOSITORY_LINK $INSTALLATION_PATH || {
    echo "git clone of crypto-methods repo failed!"
    exit 1
}

cd $INSTALLATION_PATH

# Checking if python3 is installed
command_exists python3 || {
    echo "Python3 is not installed!"
    echo "Install python3 and try again..."
    exit 1
}

command_exists pip3 || {
    echo "pip3 is not installed!"
    echo "Install pip3 and try again..."
    exit 1
}

# Checking for developer mode
echo "Install in developer mode? (y|N)"
read answer

case $answer in
    "y")
        REQUIREMENTS_FILE="requirements-dev.txt"
        ;;
esac

python3 -m venv venv && \
source ./venv/bin/activate && \
pip install -U pip && \
pip install -r $REQUIREMENTS_FILE && \
deactivate || {
    echo "Error creating virtual environment and installing libraries!"
    exit 1
}

echo "Completed successfully!"
