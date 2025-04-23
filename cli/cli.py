#!/bin/python3
import os
import sys
import json
import requests
import readline
import signal
import termios
import tty
import atexit
import ssl
from colorama import init, Fore, Style
from src.game import create_match, connect_match
from src.matchmaking import matchmaking
from src.badapple.player import play_badapple

# Initialize colorama
init(autoreset=True)

# Disable insecure request warnings (optional for clean output)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# SSL verification toggle
VERIFY_SSL = False  # Set to True in production

# Input history setup
HISTORY_FILE = os.path.expanduser("~/.cli_history")
try:
    readline.read_history_file(HISTORY_FILE)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, HISTORY_FILE)


def fetch_api_data(url, params=None):
    try:
        response = requests.get(url, params=params, verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def post_api_data(api_url, endpoint, data, cookies=None):
    url = f"{api_url.rstrip('/')}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    session = requests.Session()
    response = session.post(url, json=data, headers=headers, cookies=cookies, verify=VERIFY_SSL)
    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}


def login(api_url):
    def get_password(prompt):
        print(prompt, end='', flush=True)
        password = ''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ['\r', '\n']:
                    print('')
                    break
                elif ch == '\x03':
                    raise KeyboardInterrupt
                elif ch == '\x7f':
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    password += ch
                    sys.stdout.write('*')
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return password

    while True:
        try:
            username = input("Enter username: ").strip()
            password = get_password("Enter password: ")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

        payload = {"username": username, "password": password}
        session = requests.Session()
        response = session.post(
            f"{api_url.rstrip('/')}/login",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            verify=VERIFY_SSL
        )

        try:
            result = response.json()
        except ValueError:
            print("Invalid JSON response.")
            continue

        if not response.ok or not result.get("success", False):
            print("Error:", result.get("error", "Unknown error"))
            continue

        cookies = session.cookies.get_dict()
        print("Login successful!")
        return cookies, username


def read_manual(command):
    path = os.path.join("man", f"{command}.txt")
    if os.path.exists(path):
        with open(path, "r") as file:
            print(file.read())
    else:
        print(f"{Fore.YELLOW}No manual entry for: {command}{Style.RESET_ALL}")


def signal_handler(sig, frame):
    print(f"\n{Fore.MAGENTA}Ctrl-C pressed. Exiting gracefully...{Style.RESET_ALL}")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def cli_prompt(api_url, cookie, username, url):
    while True:
        try:
            command = input(f"{Fore.GREEN}({username}) > {Style.RESET_ALL}").strip().lower()
        except KeyboardInterrupt:
            print(f"\n{Fore.MAGENTA}Ctrl-C pressed. Exiting CLI...{Style.RESET_ALL}")
            break

        if command == "exit":
            print(f"{Fore.MAGENTA}Goodbye!{Style.RESET_ALL}")
            break

        elif command == "help":
            read_manual("help")

        elif command.startswith("help "):
            _, cmd = command.split(" ", 1)
            read_manual(cmd)

        elif command == "login":
            cookie, username = login(api_url)

        elif command == "apple":
            play_badapple()

        elif command == "play local":
            print(f"{Fore.BLUE}Starting local game...{Style.RESET_ALL}")
            try:
                session = requests.Session()
                session.cookies.update(cookie)
                match_data = create_match(api_url, session)
                if match_data and "data" in match_data:
                    match_id = match_data["data"].get("match_id")
                    if match_id:
                        connect_match(match_id, "Player1", "Player2", "all", cookie, url)
                    else:
                        print(f"{Fore.RED}Match ID not found in response.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to create match.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error during local match: {e}{Style.RESET_ALL}")

        elif command == "play online":
            print(f"{Fore.BLUE}Starting online game...{Style.RESET_ALL}")
            try:
                session = requests.Session()
                session.cookies.update(cookie)
                match_id, side = matchmaking(cookie, url)
                if match_id:
                    connect_match(match_id, "Player1", "Player2", side, cookie, url)
                else:
                    print(f"{Fore.RED}Match ID not found in response.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error during online match: {e}{Style.RESET_ALL}")

        else:
            print(f"{Fore.YELLOW}Unknown command. Type 'help' for assistance.{Style.RESET_ALL}")


def main():
    print(f"{Fore.MAGENTA}Welcome to the CLI! Here is the help manual:{Style.RESET_ALL}")
    read_manual("title")

    while True:
        try:
            api_url = input(f"{Fore.CYAN}Enter API URL: {Style.RESET_ALL}").strip()
            url = api_url
            api_url = api_url + '/api/'
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

        try:
            response = requests.get(api_url, verify=VERIFY_SSL)
            if response.status_code == 404:
                print(f"{Fore.RED}Error: API returned 404 Not Found. Please enter a valid URL.{Style.RESET_ALL}")
                continue
            print(f"{Fore.GREEN}API URL is valid.{Style.RESET_ALL}")
            break
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Failed to connect: {e}{Style.RESET_ALL}")

    if not VERIFY_SSL:
        print(f"{Fore.YELLOW}⚠ SSL verification is disabled. This is unsafe for production!{Style.RESET_ALL}")

    cookie, username = login(api_url)
    cli_prompt(api_url, cookie, username, url)


if __name__ == "__main__":
    main()
