import os
import csv
import re

CSV_FILE = "./../assets/languages/languages.csv"

def load_translations():
    translations = {}
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # First row contains languages
        for row in reader:
            key = row[0]
            translations[key] = {headers[i]: row[i] for i in range(1, len(row))}
    return translations, headers[1:]

def update_html_files(translations):
    html_files = [f for f in os.listdir() if f.endswith(".html")]
    
    for filename in html_files:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        
        for key, lang_values in translations.items():
            pattern = re.escape(lang_values["English"])  # Match English text
            replacement = f'<span data-lang="{key}">{lang_values["English"]}</span>'
            content = re.sub(pattern, replacement, content)
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Updated {filename}")

def main():
    translations, languages = load_translations()
    update_html_files(translations)
    print("All HTML files updated successfully.")

if __name__ == "__main__":
    main()

