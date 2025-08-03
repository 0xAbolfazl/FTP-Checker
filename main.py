from ftplib import FTP, error_perm
import socket
import argparse
from colorama import Fore, Style
import sys
from pyfiglet import Figlet

credential = []
total_scan = 0
successful = 0
failed = 0

def print_banner():
    """Display a colorful ASCII art banner for the FTP Checker"""
    f = Figlet(font='slant')  
    banner_text = f.renderText('FTP CHECKER')
    print(Fore.RED + banner_text)
    print(Fore.CYAN + "-" * 70)
    print(Fore.LIGHTWHITE_EX + "Developed by 0xAbolfazl".center(70))
    print(Fore.CYAN + "-" * 70 + "\n")

def check_ftp(host, port=21, username=None, password=None, timeout=10):
    print(f"{Fore.LIGHTBLUE_EX}----------------------------------------{Style.RESET_ALL}")
    try:
        # connect to ftp server
        with FTP(timeout=timeout) as ftp:
            ftp.connect(host, port)
            print(f"{Fore.GREEN}[+] Connected to {host}:{port}{Style.RESET_ALL}")
            
            # anon Login
            if username is None and password is None:
                try:
                    ftp.login()
                    print(f"{Fore.CYAN}    Anonymous login successful!{Style.RESET_ALL}")
                    return True
                except error_perm:
                    print(f"{Fore.RED}    Anonymous login failed{Style.RESET_ALL}")
                    return False
            
            # Login with specific username and password
            try:
                ftp.login(username, password)
                print(f"{Fore.CYAN}    Login successful with {username}:{password}{Style.RESET_ALL}")
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
    try:
        print(f'{Fore.BLUE}[+] Reading file data ....{Style.RESET_ALL}')
        with open(path, 'r') as file:
            data = file.readlines()
            for index, item in enumerate(data):
                item = item.strip()
                try:
                    credential.append({'host':item.split('|')[0],
                                    'port':item.split('|')[1],
                                    'username':item.split('|')[2],
                                    'password':item.split('|')[3]})
                    print(f'{Fore.BLUE}Reading data finished{Style.RESET_ALL}')
                except Exception:
                    print(f'{Fore.RED}[!] Invalid data format, your credential should be in this foramt :\nhost|port|username|password{Style.RESET_ALL}')
                    sys.exit(0)
    except Exception:
        print(f'{Fore.RED}[!] File not exists !{Style.RESET_ALL}')
        sys.exit(0)

def main():
    global successful, failed, total_scan 
    
    print_banner()

    parser = argparse.ArgumentParser(description='FTP Checker Tool')
    parser.add_argument('-f', '--file', help='File name')
    args = parser.parse_args()

    if args.file:
        file_path = args.file
    else:
        file_path = input('[-] Enter your file path : ')

    read_file(file_path)
    total_scan = len(credential)

    for i in credential:
        if check_ftp(host=i['host'],
                  port=int(i['port']) if i['port'] else 21,
                  username=i['username'],
                  password=i['password']):
            successful += 1
        else:
            failed += 1
    
    print(f'Result : \n    Total scan : {total_scan}\n    {Fore.GREEN}Successful : {successful}{Style.RESET_ALL}\n    {Fore.RED}Failed  : {failed}{Style.RESET_ALL}')

if __name__ == "__main__":
    main()