from bs4 import BeautifulSoup
import os
import sys

# Use the current working directory as the folder containing HTML files
html_folder = os.getcwd()

def add_accessibility(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return

    # Add aria-labels to buttons if missing
    for button in soup.find_all("button"):
        if not button.has_attr("aria-label"):
            # Using the button text as a label (if present) or a default placeholder.
            button_text = button.get_text(strip=True)
            button["aria-label"] = button_text if button_text else "Button"

    # Ensure images have alt text
    for img in soup.find_all("img"):
        if not img.has_attr("alt"):
            img["alt"] = "Description of image"  # Consider customizing this based on context.

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(str(soup))
        print(f"Updated accessibility for: {file_path}")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}", file=sys.stderr)

def main():
    # Get all files in the current directory and process only those ending with .html
    for filename in os.listdir(html_folder):
        if filename.lower().endswith(".html"):
            file_path = os.path.join(html_folder, filename)
            add_accessibility(file_path)

    print("Accessibility updates applied successfully!")

if __name__ == "__main__":
    main()

