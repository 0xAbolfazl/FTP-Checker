from ftplib import FTP, error_perm
import socket
import argparse
from colorama import Fore, Style
import sys
from pyfiglet import Figlet

# Global variables
credential = []  # Stores credentials from input file
total_scan = 0   # Total number of scans attempted
successful = 0   # Count of successful logins
failed = 0       # Count of failed logins
VALID_CREDENTIALS_FILE = "valid_credentials.txt"  # File to save successful logins

def print_banner():
    """Display a colorful ASCII art banner for the FTP Checker"""
    f = Figlet(font='slant')  
    banner_text = f.renderText('FTP CHECKER')
    print(Fore.RED + banner_text)
    print(Fore.CYAN + "-" * 70)
    print(Fore.LIGHTWHITE_EX + "Developed by 0xAbolfazl".center(70))
    print(Fore.CYAN + "-" * 70 + "\n")

def save_valid_credential(host, port, username, password):
    """Save valid credentials to file in host|port|username|password format"""
    with open(VALID_CREDENTIALS_FILE, 'a') as f:
        # Handle anonymous login case (empty username/password)
        cred_line = f"{host}|{port}|{username if username else ''}|{password if password else ''}\n"
        f.write(cred_line)
        print(f"{Fore.GREEN}[+] Saved valid credentials to {VALID_CREDENTIALS_FILE}{Style.RESET_ALL}")

def check_ftp(host, port=21, username=None, password=None, timeout=10):
    """
    Attempt FTP connection and login
    Returns True if successful, False otherwise
    """
    print(f"{Fore.LIGHTBLUE_EX}----------------------------------------{Style.RESET_ALL}")
    try:
        # Connect to FTP server
        with FTP(timeout=timeout) as ftp:
            ftp.connect(host, port)
            print(f"{Fore.GREEN}[+] Connected to {host}:{port}{Style.RESET_ALL}")
            
            # Attempt anonymous login if no credentials provided
            if username is None and password is None:
                try:
                    ftp.login()
                    print(f"{Fore.CYAN}    Anonymous login successful!{Style.RESET_ALL}")
                    save_valid_credential(host, port, None, None)  # Save with empty credentials
                    return True
                except error_perm:
                    print(f"{Fore.RED}    Anonymous login failed{Style.RESET_ALL}")
                    return False
            
            # Attempt login with provided credentials
            try:
                ftp.login(username, password)
                print(f"{Fore.CYAN}    Login successful with {username}:{password}{Style.RESET_ALL}")
                save_valid_credential(host, port, username, password)
                return True
            except error_perm as e:
                print(f"{Fore.RED}    Login failed with {username}:{password} - {str(e)}{Style.RESET_ALL}")
                return False
                
    except socket.timeout:
        print(f"{Fore.RED}[-] Connection timeout for {host}:{port}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[-] Error connecting to {host}:{port} - {str(e)}{Style.RESET_ALL}")
        return False
    finally:
        print(f"{Fore.LIGHTBLUE_EX}----------------------------------------{Style.RESET_ALL}")

def read_file(path):
    """
    Read credentials from input file
    Expected format: host|port|username|password per line
    """
    try:
        print(f'{Fore.BLUE}[+] Reading file data ....{Style.RESET_ALL}')
        with open(path, 'r') as file:
            data = file.readlines()
            for item in data:
                item = item.strip()
                try:
                    # Split line into components
                    parts = item.split('|')
                    if len(parts) != 4:
                        raise ValueError("Invalid number of parts")
                    
                    credential.append({
                        'host': parts[0],
                        'port': parts[1],
                        'username': parts[2],
                        'password': parts[3]
                    })
                except Exception:
                    print(f'{Fore.RED}[!] Invalid data format, your credential should be in this format:\nhost|port|username|password{Style.RESET_ALL}')
                    sys.exit(0)
        print(f'{Fore.BLUE}[+] Reading data finished - {len(credential)} credentials loaded{Style.RESET_ALL}')
    except Exception:
        print(f'{Fore.RED}[!] File not exists or cannot be read!{Style.RESET_ALL}')
        sys.exit(0)

def main():
    global successful, failed, total_scan 
    
    print_banner()

    # Initialize empty valid credentials file
    open(VALID_CREDENTIALS_FILE, 'w').close()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='FTP Checker Tool')
    parser.add_argument('-f', '--file', help='Input file containing credentials (host|port|username|password per line)')
    args = parser.parse_args()

    # Get input file path
    if args.file:
        file_path = args.file
    else:
        file_path = input('[-] Enter your file path: ')

    # Read credentials from file
    read_file(file_path)
    total_scan = len(credential)

    # Process each credential
    for cred in credential:
        if check_ftp(
            host=cred['host'],
            port=int(cred['port']) if cred['port'] else 21,
            username=cred['username'] if cred['username'] else None,
            password=cred['password'] if cred['password'] else None
        ):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    print(f'\nResult: \n    Total scan: {total_scan}\n    {Fore.GREEN}Successful: {successful}{Style.RESET_ALL}\n    {Fore.RED}Failed: {failed}{Style.RESET_ALL}')
    print(f"{Fore.YELLOW}[*] Valid credentials saved to {VALID_CREDENTIALS_FILE}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()