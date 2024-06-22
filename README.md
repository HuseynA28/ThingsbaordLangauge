# Locale Translator

This project is designed to translate JSON files containing localized strings into different languages using the DeepL API. The script processes HTML-like content within the JSON strings to ensure proper translation of text without breaking the HTML structure.

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)

## Setup

1. Clone the repository or download the script.
2. Install the required library:
    ```sh
    pip install requests
    ```
3. Obtain a DeepL API key from [DeepL](https://www.deepl.com/pro-api).
4. Prepare the JSON files you want to translate. Ensure they are in the same directory as the script or update the file paths accordingly.

## Usage

1. Replace the `api_key` variable with your actual DeepL API key in the `main.py` script:
    ```python
    api_key = "YOUR_ACTUAL_DEEPL_API_KEY"  # Replace this with your actual DeepL API key
    ```
2. Update the `original_json_file` variable with the name of your original JSON file:
    ```python
    original_json_file = "locale.constant-en_US.json"  # Adjust the file name/path as needed
    ```
3. Define the list of languages you want to translate into by modifying the `languages` list:
    ```python
    languages = ["EN"]  # Add or remove language codes as needed
    ```
4. Run the script:
    ```sh
    python main.py
    ```

## Script Overview

### `main.py`
