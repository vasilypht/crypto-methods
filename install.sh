#!/bin/sh

REPOSITORY_LINK=https://github.com/vasilypht/crypto-methods.git 
INSTALLATION_PATH=$HOME/crypto-methods

# check for installed git
if ! command -v git &>/dev/null; then
    echo "git is not installed!"
    echo "Install git and try again..."
    exit 1
fi

git clone $REPOSITORY_LINK $INSTALLATION_PATH
cd $INSTALLATION_PATH

if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed!"
    echo "Install python3 and try again..."
    exit 1
fi

python3 -m venv venv
source ./venv/bin/activate
pip install -U pip
pip install -r requirements.txt

echo "Completed successfully!"
