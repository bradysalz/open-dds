#!/usr/bin/env bash
set -euf -o pipefail

# Cocotb prerequisites
sudo apt-get install python3-dev

# Verilator prerequisites:
sudo apt-get install git make autoconf g++ flex bison 
sudo apt-get install libfl2  # Ubuntu only (ignore if gives error)
sudo apt-get install libfl-dev  # Ubuntu only (ignore if gives error)

# Don't clone unless we need it
if [ ! -d "verilator" ]; then
    git clone https://github.com/verilator/verilator   
fi 

# Every time you need to build:
unset VERILATOR_ROOT  # For bash
cd verilator
git pull        # Make sure git repository is up-to-date
git checkout stable      # Use most recent stable release

autoconf     # Create ./configure script
./configure
make
sudo make install
