#!/usr/bin/env bash

set -e

# change working directory to this script's path
cd "$(dirname "$0")"
      

printf "Setting up python environment...🏎️\n"

python3 -m venv .venv
source .venv/bin/activate
pip3 --disable-pip-version-check -q install -r requirements.txt

printf "Local python environment setup complete🏁\n"

printf "Starting the Bot....🚀\n"

python3 bot/bot.py
