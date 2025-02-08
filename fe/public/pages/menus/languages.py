import os
import glob
import csv
from bs4 import BeautifulSoup

# ---- 1. Load translations from CSV ----
csv_filename = "../../assets/languages/languages.csv"  # CSV format: key,english,spanish,ukrainian,...
translations = {}
with open(csv_filename, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Expecting: key, english, spanish, ukranian, ...
    # Use the first language column (after the key) as the default.
    default_language = headers[1].strip().lower()
    for row in reader:
        if not row or not row[0].strip():
            continue
        key = row[0].strip()
        translations[key] = {}
        for i, lang in enumerate(headers[1:]):
            translations[key][lang.strip().lower()] = row[i + 1].strip() if i + 1 < len(row) else ""

# --- 2. Build a reverse lookup from the default (English) text to its key ---
# For example, if the CSV row is:
# edit-username,Username,Nombre de usuario,Ім'я користувача
# then we map "username" (lowercased and stripped) to "edit-username".
english_to_key = {}
for key, lang_dict in translations.items():
    eng_text = lang_dict.get(default_language, "").strip()
    if eng_text:
        english_to_key[eng_text.lower()] = key

# --- 3. Define a helper function to determine a candidate translation key ---
def get_translation_candidate(el):
    """
    For a given BeautifulSoup element, try to determine a translation key.
    It first checks for candidate attributes that are meant to store keys (like data-modal or id).
    If none are found, it checks whether the element’s visible text (or for inputs/images, a related attribute)
    matches one of the default (English) texts from the CSV.
    Returns a tuple (key, target) where:
      - key: the translation key from CSV, or None if not found.
      - target: which property should be updated ("innerHTML", "value", "alt", or "aria-label").
    """
    # Skip if already marked
    if el.has_attr("data-i18n"):
        return None, None

    # Candidate 1: if the element has a data-modal attribute and its value is a known key.
    if el.has_attr("data-modal"):
        candidate = el["data-modal"].strip()
        if candidate in translations:
            return candidate, "innerHTML"

    # Candidate 2: if the element has an id attribute that is a known key.
    if el.has_attr("id"):
        candidate = el["id"].strip()
        if candidate in translations:
            return candidate, "innerHTML"

    # Candidate 3: For input elements (button, submit, reset), check the value attribute.
    if el.name == "input" and el.get("type", "").lower() in ['button', 'submit', 'reset'] and el.has_attr("value"):
        candidate = el["value"].strip()
        if candidate.lower() in english_to_key:
            return english_to_key[candidate.lower()], "value"

    # Candidate 4: For images, check the alt attribute.
    if el.name == "img" and el.has_attr("alt"):
        candidate = el["alt"].strip()
        if candidate.lower() in english_to_key:
            return english_to_key[candidate.lower()], "alt"

    # Candidate 5: Check the aria-label attribute.
    if el.has_attr("aria-label"):
        candidate = el["aria-label"].strip()
        if candidate.lower() in english_to_key:
            return english_to_key[candidate.lower()], "aria-label"

    # Candidate 6: Check the element’s inner text.
    text = el.get_text(strip=True)
    if text:
        if text.lower() in english_to_key:
            return english_to_key[text.lower()], "innerHTML"

    return None, None

# --- 4. Process every HTML file in the current directory ---
html_files = glob.glob("*.html")

for filename in html_files:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    modified = False

    # Process every element in the document
    for el in soup.find_all(True):
        key, target = get_translation_candidate(el)
        if key:
            # Mark the element with the translation key.
            el["data-i18n"] = key

            # Update the element’s text or attribute with the default (English) translation.
            new_text = translations[key].get(default_language, "")
            if new_text:
                if target == "innerHTML":
                    el.string = new_text
                else:
                    el[target] = new_text
            modified = True

    if modified:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Processed and updated: {filename}")
    else:
        print(f"No matching translation found in: {filename}")
