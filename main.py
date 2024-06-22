import json
import requests
from html.parser import HTMLParser

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.last_tag = ""

    def handle_data(self, data):
        self.text_parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in ["br", "img", "hr"]:
            self.text_parts.append(f"<{tag}/>")
        else:
            self.text_parts.append(f"<{tag}>")
            self.last_tag = tag

    def handle_endtag(self, tag):
        if tag not in ["br", "img", "hr"]:
            self.text_parts.append(f"</{tag}>")

    def get_data(self):
        return ''.join(self.text_parts)

def translate_text(text, api_key, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"DeepL-Auth-Key {api_key}"
    }
    data = {
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['translations'][0]['text']

def translate_html_safe(text, api_key, target_lang):
    parser = HTMLTextExtractor()
    parser.feed(text)
    text_parts = parser.text_parts
    translated_parts = []
    for part in text_parts:
        if '<' in part:
            translated_parts.append(part)
        else:
            translated_parts.append(translate_text(part, api_key, target_lang))
    return ''.join(translated_parts)

def translate_json_values(json_data, api_key, target_lang, total_elements, translated_elements, last_reported_progress):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            json_data[key], total_elements, translated_elements, last_reported_progress = translate_json_values(value, api_key, target_lang, total_elements, translated_elements, last_reported_progress)
    elif isinstance(json_data, list):
        for index, item in enumerate(json_data):
            json_data[index], total_elements, translated_elements, last_reported_progress = translate_json_values(item, api_key, target_lang, total_elements, translated_elements, last_reported_progress)
    elif isinstance(json_data, str):
        translated_data = translate_html_safe(json_data, api_key, target_lang)
        translated_elements += 1
        progress = (translated_elements / total_elements) * 100
        if progress - last_reported_progress >= 10:
            print(f"Progress: {int(progress)}%")
            last_reported_progress = progress
        return translated_data, total_elements, translated_elements, last_reported_progress
    return json_data, total_elements, translated_elements, last_reported_progress

def count_elements(json_data):
    if isinstance(json_data, dict):
        return sum(count_elements(value) for value in json_data.values())
    elif isinstance(json_data, list):
        return sum(count_elements(item) for item in json_data)
    elif isinstance(json_data, str):
        return 1
    return 0

def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

api_key = "XXXXXX"  # Replace this with your actual DeepL API key
original_json_file = "locale.constant-en_US.json"  # Adjust the file name/path as needed

# Define the list of languages to translate into
languages = ["SK", "SV"]

# Read the original JSON data
data = read_json(original_json_file)

# Translate and save for each language
for lang in languages:
    total_elements = count_elements(data)
    translated_data, _, _, _ = translate_json_values(data, api_key, lang, total_elements, 0, 0)
    translated_json_file = f"locale.constant-{lang}.json"
    write_json(translated_data, translated_json_file)
    print("Translation completed and saved to:", translated_json_file)
