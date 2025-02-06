from bs4 import BeautifulSoup # type: ignore
import re
import json
import random
import string


# Function to remove tags
def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)

def removeNewLine(text):
    return re.sub(r"\n", "", text)

def remove_double_space(text):
    return re.sub(r'\s+', ' ', text)

def remove_between_parens_and_braces(text):
    return re.sub(r'\[\s*\{', '[{', text)
    
def remove_between_braces_and_parens(text):
    return re.sub(r'\}\s*\]', '}]', text)

def extract_data_from_text(text):
    text = removeNewLine(text)
    text = remove_double_space(text)
    text = remove_between_parens_and_braces(text)
    text = remove_between_braces_and_parens(text)
    start_index = text.find('[{')
    end_index = text.rfind('}]') + 2  # Tambah 2 untuk mencakup karakter '}]'
    json_str = text[start_index:end_index]
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Terjadi kesalahan saat mem-parsing JSON:", e, text)
        return []
    return data

def remove_think_tags(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

def space_to_under(text):
    return re.sub(r"\s+", "_", text)


def generate_random_string(length=8):

    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))
    # all_characters = string.ascii_letters + string.digits + string.punctuation
    # return ''.join(random.choice(all_characters) for _ in range(length))