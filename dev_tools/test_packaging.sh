#!/bin/bash -e

#------------------------------------------------------------------------------
# Py2C - A Python to C++ compiler
# Copyright (C) 2014 Pradyun S. Gedam
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# A script that generates the source distribution in a clean venv and tests it.
# Requires:
#   - virtualenvwrapper to be installed and source'd beforehand.
#   - Current working directory is the root of the project.
#------------------------------------------------------------------------------

# Create a temporary venv (with virtualenvwrapper) and come back to same directory
pushd /tmp > /dev/null
echo -e -n "\e[1;33mMaking temporary virtualenv for the build...\e[0m"
mktmpenv > /dev/null
echo -e "\e[1;32mDone\e[0m"
popd > /dev/null

# Delegated to a python script...
python ./dev_tools/check_packaging.py

echo -e -n "\e[1;33mDeleting temporary virtualenv...\e[0m"
deactivate > /dev/null
echo -e "\e[1;32mDone\e[0m"