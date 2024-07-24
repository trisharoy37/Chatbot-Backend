#!/usr/bin/env bash

# Install dependencies
sudo apt-get update
sudo apt-get install -y wget build-essential libreadline-dev

# Download and install SQLite3
SQLITE_VERSION=3.40.1  # replace with the version you need
wget https://www.sqlite.org/2023/sqlite-autoconf-${SQLITE_VERSION//./}000.tar.gz
tar xzf sqlite-autoconf-${SQLITE_VERSION//./}000.tar.gz
cd sqlite-autoconf-${SQLITE_VERSION//./}000
./configure
make
sudo make install

# Verify installation
sqlite3 --version
