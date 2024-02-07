import itertools
import requests
from bs4 import BeautifulSoup

def generate_combinations(letters):
    combinations = set()

    for r in range(1, len(letters) + 1):
        for subset in itertools.permutations(letters, r):
            combinations.add(''.join(subset))

    return combinations

def find_valid_words(letters, valid_words, oxford_word_list=None):
    letters = ''.join(letters).lower()  # Convert the input letters to lowercase
    combinations = generate_combinations(letters)
    valid_matches = [w for w in combinations if w.lower() in map(str.lower, valid_words)]
    answers = []
    if oxford_word_list:
        for word in valid_matches:
            if word in oxford_word_list:
                answers.append(word)
    else:
        print("Failed to retrieve the word list.")

    return valid_matches

def get_oxford_word_list():
    url = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    words = []

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            selector = soup.find('ul', class_='top-g')
            
            if selector:
                list_items = selector.find_all('li')
                for item in list_items:
                    word = item.text.strip().split()[0]
                    words.append(word)
            else:
                print("No unordered list with class 'wordlist' found on the page.")
            
            return words
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

with open('./Data/eowl.txt', 'r', encoding='utf-8') as file:
    english_words = set(file.read().splitlines())

inp = input("Enter the letters you want to scrape: ")

oxford_word_list = get_oxford_word_list()
if oxford_word_list:
    result = find_valid_words(list(inp), english_words, oxford_word_list)
    print(result)
