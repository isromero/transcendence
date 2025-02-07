import glob
import csv
from bs4 import BeautifulSoup

def extract_relevant_text():
    # Use a set to check for duplicates and a list to preserve order
    seen = set()
    texts = []
    
    # Get all HTML files in the current directory
    html_files = glob.glob("*.html")
    
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # --- Extract text from specific elements ---

        # 1. Get the content of the <title> tag, if any.
        if soup.title and soup.title.string:
            text = soup.title.string.strip()
            if text and text not in seen:
                seen.add(text)
                texts.append(text)
        
        # 2. Get the meta description (if exists)
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            text = meta_desc["content"].strip()
            if text and text not in seen:
                seen.add(text)
                texts.append(text)
        
        # --- Remove non-visible elements ---
        # Remove script and style tags since their text is not visible.
        for tag in soup(["script", "style"]):
            tag.decompose()
        
        # --- Extract visible text ---
        # .stripped_strings yields only non-empty strings with extra whitespace removed.
        for string in soup.stripped_strings:
            text = string.strip()
            if text and text not in seen:
                seen.add(text)
                texts.append(text)
        
        # --- Extract button texts explicitly (if not already caught) ---
        for button in soup.find_all("button"):
            text = button.get_text(strip=True)
            if text and text not in seen:
                seen.add(text)
                texts.append(text)
        
        # --- Extract text from input buttons ---
        # Sometimes buttons are not <button> elements but <input> elements with a value.
        for input_tag in soup.find_all("input"):
            if input_tag.has_attr("type") and input_tag["type"].lower() in ["button", "submit", "reset"]:
                text = input_tag.get("value", "").strip()
                if text and text not in seen:
                    seen.add(text)
                    texts.append(text)
                    
    return texts

def write_to_csv(text_list, output_filename="output.csv"):
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write each unique string with an incrementing id (starting from 1)
        for idx, text in enumerate(text_list, 1):
            writer.writerow([idx, text])

if __name__ == "__main__":
    extracted_texts = extract_relevant_text()
    write_to_csv(extracted_texts)
    print(f"Extracted {len(extracted_texts)} unique text strings into output.csv")

