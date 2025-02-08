import glob
import csv
from bs4 import BeautifulSoup, NavigableString

# --- 1. Load translations from CSV ---
# CSV Format example:
# key,english,spanish,ukrainian
# login,Login,Iniciar sesión,Вхід
# signup,Sign Up,Regístrate,Реєстрація
csv_filename = "../../assets/languages/languages.csv"
translations = {}

with open(csv_filename, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Expecting: key, english, spanish, ukranian, ...
    default_language = headers[1].strip().lower()
    for row in reader:
        if not row or not row[0].strip():
            continue
        key = row[0].strip()
        translations[key] = {}
        for i, lang in enumerate(headers[1:]):
            translations[key][lang.strip().lower()] = row[i+1].strip() if i+1 < len(row) else ""

# --- 2. Build a reverse lookup from default text (e.g. English) to its key ---
english_to_key = {}
for key, lang_dict in translations.items():
    eng_text = lang_dict.get(default_language, "").strip()
    if eng_text:
        english_to_key[eng_text.lower()] = key

# --- 3. Helper: Check if an element is a leaf (i.e. it does not have child tags) ---
def is_leaf_element(el):
    return not any(getattr(child, 'name', None) for child in el.contents)

# --- 4. Candidate selection function ---
def get_translation_candidate(el):
    """
    For a given element, try to determine a translation candidate.
    This function checks attributes in a certain order.
    If the element is a container (e.g. <a> that has a <button> child),
    we skip it so that the nested element can be processed instead.
    Returns a tuple (key, target) where target is one of:
      "innerHTML", "aria-label", "value", or "alt".
    """
    # Skip if already marked.
    if el.has_attr("data-i18n"):
        return None, None

    # **Skip container elements that hold a translatable child.**
    # For example, if an <a> wraps a <button>, let the <button> be updated.
    if el.name == "a" and el.find("button"):
        return None, None

    # Candidate 1: data-modal attribute (if present and valid)
    if el.has_attr("data-modal"):
        candidate = el["data-modal"].strip()
        if candidate in translations:
            return candidate, "innerHTML"

    # Candidate 2: id attribute
    if el.has_attr("id"):
        candidate = el["id"].strip()
        if candidate in translations:
            return candidate, "innerHTML"

    # Candidate 3: For input elements (buttons) – check the value attribute.
    if el.name == "input" and el.get("type", "").lower() in ['button', 'submit', 'reset'] and el.has_attr("value"):
        candidate = el["value"].strip()
        if candidate.lower() in english_to_key:
            return english_to_key[candidate.lower()], "value"

    # Candidate 4: For images – check the alt attribute.
    if el.name == "img" and el.has_attr("alt"):
        candidate = el["alt"].strip()
        if candidate.lower() in english_to_key:
            return english_to_key[candidate.lower()], "alt"

    # Candidate 5: Check aria-label attribute.
    if el.has_attr("aria-label"):
        candidate = el["aria-label"].strip()
        if candidate.lower() in english_to_key:
            return english_to_key[candidate.lower()], "aria-label"

    # Candidate 6: Check inner text, but only if the element is a leaf (to avoid replacing nested structures).
    text = el.get_text(strip=True)
    if text and is_leaf_element(el):
        if text.lower() in english_to_key:
            return english_to_key[text.lower()], "innerHTML"

    return None, None

# --- 5. Process every HTML file in the current directory ---
html_files = glob.glob("*.html")

for filename in html_files:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    modified = False

    # Iterate over all elements.
    for el in soup.find_all(True):
        key, target = get_translation_candidate(el)
        if key:
            # Mark the element with the translation key.
            el["data-i18n"] = key

            # Get the default text for the key.
            new_text = translations[key].get(default_language, "")
            if new_text:
                if target == "innerHTML":
                    # Only update inner text if this element is a leaf.
                    if is_leaf_element(el):
                        el.string = new_text
                else:
                    el[target] = new_text
            modified = True

    # Write back the modified HTML if any changes were made.
    if modified:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Processed and updated: {filename}")
    else:
        print(f"No matching translation found in: {filename}")

