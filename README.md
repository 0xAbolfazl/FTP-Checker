# FTP Checker Tool

A Python script to validate FTP credentials and check server accessibility.

## Features

- Test FTP server connections
- Support both anonymous and authenticated logins
- Read credentials from file or command line input
- Save valid credentials to `valid_credentials.txt`
- Colorful console output with statistics

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/ftp-checker.git
    cd ftp-checker

2. Install required packages:

    ```bash
    pip install -r requirements.txt

## Usage

Basic Usage
    ```bash
    python ftp_checker.py -f credentials.txt

## Input File Format

Create a text file with credentials in this format (one per line):
```plaintext
ftp.example.com|21|admin|password
ftp.test.com|2121|anonymous|
192.168.1.100|21||
```

## Output

Valid credentials are saved to valid_credentials.txt in same format

- Console shows color-coded results:
- Green: Successful connections
- Red: Failed attempts
- Blue: Informational messages

## Requirements

Python 3.6+
Required packages:
    - ftplib
    - colorama
    - pyfiglet
