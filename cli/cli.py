#!/bin/python3
import requests
import json
import os
from src.game import create_match, connect_match
from src.matchmaking import matchmaking

def fetch_api_data(url, params=None):
    try:
        response = requests.get(url, params=params)
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
        print("Login successful!")
        return cookies, username

def read_manual(command):
    path = f"./man/{command}.txt"
    if os.path.exists(path):
        with open(path, "r") as file:
            print(file.read())
    else:
        print("No manual entry for:", command)

def cli_prompt(api_url, cookie, username):
    while True:
        command = input(f"({username}) > ").strip().lower()

        if command == "exit":
            print("Goodbye!")
            break

        elif command == "help":
            read_manual("help")

        elif command.startswith("help "):
            _, cmd = command.split(" ", 1)
            read_manual(cmd)

        elif command == "login":
            cookie, username = login(api_url)

        elif command == "play local":
            print("Starting local game...")
            try:
                session = requests.Session()
                session.cookies.update(cookie)
                match_data = create_match(api_url, session)
                if match_data and "data" in match_data:
                    match_id = match_data["data"].get("match_id")
                    if match_id:
                        connect_match(match_id, "Player1", "Player2", "all")
                    else:
                        print("Match ID not found in response.")
                else:
                    print("Failed to create match.")
            except Exception as e:
                print("Error during local match:", e)

        elif command == "play online":
            print("Starting online game...")
            try:
                session = requests.Session()
                session.cookies.update(cookie)
                match_id, side = matchmaking(cookie)
                if match_id:
                    connect_match(match_id, "Player1", "Player2", side)
                else:
                    print("Match ID not found in response.")
            except Exception as e:
                print("Error during online match:", e)

        else:
            print("Unknown command. Type 'help' for assistance.")

def main():
    while True:
        api_url = input("Enter API URL: ").strip()

        try:
            response = requests.get(api_url)
            if response.status_code == 404:
                print("Error: API returned 404 Not Found. Please enter a valid URL.")
                continue
            print("API URL is valid.")
            break
        except requests.exceptions.RequestException as e:
            print("Failed to connect:", e)

    cookie, username = login(api_url)
    cli_prompt(api_url, cookie, username)

if __name__ == "__main__":
    main()
