import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_passage(text_name, book, chapter, verse, text, context, theme, commentary, translation="King James Version", language="English"):
    if not all([text_name, book, chapter, verse, text]):
        logging.error("Missing required passage information.")
        return None
    passage = {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "text": text,
        "context": context,
        "theme": theme,
        "commentary": commentary,
        "translation": translation,
        "language": language
    }
    return text_name, passage

def update_bibliomancy(file_path, new_passages):
    # Check if the file exists
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return

    # Load the existing JSON data
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from file.")
        return

    # Ensure the 'bibliomancy' key exists
    if 'bibliomancy' not in data:
        logging.error("'bibliomancy' key not found in JSON data.")
        return

    # Add new passages to the appropriate text
    for text_name, passage in new_passages:
        if passage is None:
            continue
        if text_name not in data['bibliomancy']:
            data['bibliomancy'][text_name] = {'passages': []}
        data['bibliomancy'][text_name]['passages'].append(passage)
        logging.info(f"Added passage to {text_name}: {passage['book']} {passage['chapter']}:{passage['verse']}")

    # Backup the original file
    backup_path = file_path + '.bak'
    os.rename(file_path, backup_path)
    logging.info(f"Backup created: {backup_path}")

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    logging.info(f"Updated bibliomancy data saved to {file_path}")

# Example usage
new_passages = [
    add_passage("Bible", "Exodus", 3, 14, "And God said unto Moses, I AM THAT I AM...", "God reveals His name to Moses.", "Divine Identity", "This passage highlights the eternal and self-existent nature of God."),
    add_passage("Qur'an", "Al-Baqarah", 2, 255, "Allah! There is no deity except Him, the Ever-Living, the Sustainer of existence...", "The verse of the Throne.", "Divine Sovereignty", "This verse emphasizes the power and knowledge of Allah.")
]

# Ensure the correct path to your JSON file
update_bibliomancy('bibliomancy.json', new_passages)
