#!/bin/bash

printf "\33[1;49;95m+-- setup.sh --+\33[0m\n"

printf "\33[1;49;97mSetting bash flags...\33[0m\n"

# If an error occurrs, exit; don't carry on.
printf "\33[1;49;97m\t- Setting '-e' flag...\33[0m\n"
set -e

# Check arguments
printf "\33[1;49;97mChecking arguments...\33[0m\n"

no_probe_registry=0
only_download=0

function confirm {
    read -sp "-- Type 'exit' (all lowercase) to exit, anything else to continue: " user_input
    printf "\n"
    if [[ "$user_input" == "exit" ]]; then
        exit 0
    fi
}

if [ -n "$1" ]; then
    if [[ "$1" == "no_probe_registry" ]]; then
        printf "\33[1;49;93m\tThe 'no_probe_registry' flag is set.\33[0m\n"
        printf "\33[1;49;97m\tYou usually enable this when you have already probed the registries.\33[0m\n"
        confirm

        no_probe_registry=1
    elif [[ "$1" == "only_download" ]]; then
        printf "\33[1;49;93m\tThe 'only_download' flag is set.\33[0m\n"
        confirm

        only_download=1
    fi
fi

# Download necessary files
printf "\33[1;49;97mDownloading necessary files...\33[0m\n"
printf "\33[1;49;97m\t- 'setup_helpers/setup.py'...\33[0m\n"

if [[ "$only_download" == "1" ]]; then
    exit 0
fi

# Probe for setup registry files
if [[ "$no_probe_registry" == "0" ]]; then
    printf "\33[1;49;97mProbing for setup registry files...\33[0m\n"
    python setup_helpers/probe_reg_files.py
fi

# Load the setup
printf "\33[1;49;97mLoading setup...\33[0m\n"
printf "\33[1;49;97m-------------------------------------------\33[0m\n"
#   The setup script should usually be in
#   setup_helpers/setup.py
python setup_helpers/setup.py
