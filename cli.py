#!/bin/python3
import requests
import json
import os

def fetch_api_data(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def post_api_data(api_url, endpoint, data, cookies=None):
    url = f"{api_url.rstrip('/')}/{endpoint}"  # Ensure no double slashes
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    session = requests.Session()
    response = session.post(url, json=data, headers=headers, cookies=cookies)
    
    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

def login(api_url):
    while True:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        payload = {"username": username, "password": password}
        session = requests.Session()
        response = session.post(f"{api_url.rstrip('/')}/login", json=payload, headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        
        try:
            result = response.json()
        except ValueError:
            print("Invalid JSON response.")
            continue
        
        if not response.ok or not result.get("success", False):
            print("Error:", result.get("error", "Unknown error"))
            continue
        
        cookies = session.cookies.get_dict()
        print("Login successful! Cookies:", cookies)
        return cookies

def read_manual(command):
    path = f"./cli/man/{command}.txt"
    if os.path.exists(path):
        with open(path, "r") as file:
            print(file.read())
    else:
        print("No command found")

def cli_prompt(api_url, cookie):
    while True:
        command = input("(user) > ").strip()
        
        if command == "exit":
            break
        elif command == "help":
            read_manual("help")
        elif command.startswith("help "):
            _, cmd = command.split(" ", 1)
            read_manual(cmd)
        elif command == "login":
            cookie = login(api_url)
        elif command == "play local":
            print("Starting local game...")
        elif command == "play online":
            print("Starting online game...")
        else:
            print("Unknown command. Type 'help' for assistance.")

def main():
    while True:
        api_url = input("Enter API URL: ").strip()

        # Test if the API URL is valid
        test_response = requests.get(api_url)
        if test_response.status_code == 404:
            print("Error: API returned 404 Not Found. Please enter a valid URL.")
            continue
        else:
            print("API URL is valid.")
            break
    
    cookie = login(api_url)
    cli_prompt(api_url, cookie)

if __name__ == "__main__":
    main()
