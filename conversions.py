import pandas as pd
import re
import unicodedata

def normalize(s):
    # Use regex to match words or single punctuation marks
    result = s.lower()
    result = result.replace("e", "i")
    result = result.replace("o", "u")
    return result

def split_into_tokens(s):
    # Use regex to match words or single punctuation marks
    tokens = re.findall(r"\b[\w']+\b|[^\w\s]", s)
    cleaned_tokens = [token.replace("'", "") for token in tokens]
    return cleaned_tokens

def phonemize_exceptions(tokens):
    exceptions = ["ang", "ba", "kang", "na", "ni", "pa", "ra", "sa", "si", "ug"]
    def phonemize(token):
        if token in exceptions:
            token = token.replace("ng", "ŋ")
            if token[0] in ["a", "i", "u", "á", "í", "ú"]:
                token = "q" + token
            return token + "0"
        return token
    tokens = map(phonemize, tokens)
    return tokens

def match_words_with_dataset(tokens):
    # Load the CSV file into a DataFrame
    file_path = "data/ceb_roots_filtered.csv"
    df = pd.read_csv(file_path)
    # Filter rows where the search_column matches the target word
    def match_to_dataset(token):
        filtered_rows = df[df["normalized_head"] == token]
        if len(filtered_rows) == 0:
            return token
        return filtered_rows["head"].tolist()[0]
    tokens = map(match_to_dataset, tokens)
    return tokens

# def append_numeric_to_syllable(token):
#     vowels = 'aeiouáéíóú'
#     accented_vowels = 'áéíóú'
#     # for i in range(len(token)):
#     #     if token[i] in vowels:    
#             # if token[i + 2]
#     return token

def append_numeric_to_syllable(token):
    if token[-1] in ["*", ".", ",", "0", "1", "2"]:
        return token

    if not isinstance(token, str):
        return token
    
    vowels = 'aeiouáéíóú'
    accented_vowels = 'áéíóú'
    normalize_word = unicodedata.normalize('NFC', token)
    syllables = []
    syllable_count = 0

    # Extract all syllables before the last syllables
    last_vowel_pos = -1
    current_vowel_pos = -1
    special = False
    for pointer in range(len(normalize_word) - 1, -1, -1):
        if (normalize_word[pointer] in vowels or normalize_word[pointer] in accented_vowels):
            current_vowel_pos = pointer

            # Mark the last instance of a vowel.
            if last_vowel_pos == -1:
                last_vowel_pos = pointer

            # Decide the syllable form (CVC or CV) based on closedness or openness.
            if current_vowel_pos > 1 and normalize_word[current_vowel_pos - 1] in vowels:
                # Finds a possible VC or V syllable from here. Usually at the end.
                special = True
                syllables.insert(syllable_count, normalize_word[current_vowel_pos - 2: current_vowel_pos])
                syllable_count += 1
            elif current_vowel_pos > 3 and normalize_word[current_vowel_pos - 1] not in vowels and normalize_word[current_vowel_pos - 2] not in vowels:
                # Finds a CVC syllable form here.
                syllables.insert(syllable_count, normalize_word[current_vowel_pos - 4: current_vowel_pos - 1])
                syllable_count += 1
            elif current_vowel_pos > 2 and normalize_word[current_vowel_pos - 1] not in vowels:
                # Finds a CV syllable form here.
                syllables.insert(syllable_count, normalize_word[current_vowel_pos - 3: current_vowel_pos - 1])
                syllable_count += 1

    print(syllables)

    # Extract last syllable
    if special:
        # Ensure no out of range errors when slicing
        if last_vowel_pos + 2 <= len(normalize_word):
            syllables.insert(0, normalize_word[last_vowel_pos: last_vowel_pos + 2])
        else:
            syllables.insert(0, normalize_word[last_vowel_pos:])
    else:
        # Ensure no out of range errors when slicing
        if last_vowel_pos + 2 <= len(normalize_word):
            syllables.insert(0, normalize_word[last_vowel_pos - 1: last_vowel_pos + 2])
        else:
            syllables.insert(0, normalize_word[last_vowel_pos - 1:])
        syllable_count += 1

    # Analyze each syllables
    syllables.reverse()
    processed_syllables = []
    for syllable in syllables:
        # if isinstance(syllable, str) and syllable:  # fuck Python
        #     if syllable[0] in vowels:
        #         syllable = ''.join(('q', syllable))
        if any(char in accented_vowels for char in syllable):
            if syllable == syllables[len(syllables) - 1]:
                syllable = syllable + "1"
            elif syllable == syllables[len(syllables) - 2]:
                syllable = syllable + "2"
        else:
            syllable = syllable + "0"
        processed_syllables.append(syllable)

    result = ''.join(processed_syllables)
    result = result.replace("á", "a")
    result = result.replace("í", "i")
    result = result.replace("ú", "u")
    return result

def phonemize_closed_penult(tokens):
    def add_stress_if_closed_penult(token):
        vowels = "aeiou"
        stressed_vowels = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
        
        # Function to check if a character is a consonant
        def is_consonant(char):
            return char.isalpha() and char not in vowels

        if token[-1] in ["*", ".", ",", "0", "1", "2"]:
            return token
        
        token = token.replace("ng", "ŋ")
        # Find the last vowel and its position
        last_vowel_match = re.search(r"[aeiou](?!.*[aeiou])", token) # Match the last vowel
        if not last_vowel_match:
            return token # If no vowels, return the word as is
        last_vowel_index = last_vowel_match.start()
        # Check consonants before the last vowel
        consonant_count = 0
        for i in range(last_vowel_index - 1, -1, -1):  # Iterate backwards before the last vowel
            if is_consonant(token[i]):
                consonant_count += 1
            else:
                break  # Stop counting consonants at the previous vowel or non-consonant
        # Determine where to apply stress
        if consonant_count >= 2:  # Closed syllable
            # Add stress to the penultimate vowel
            for i in range(last_vowel_index - 1, -1, -1):
                if token[i] in stressed_vowels:
                    return token[:i] + stressed_vowels[token[i]] + token[i + 1:]
        else:  # Open syllable
            # Add stress to the last vowel
            return token[:last_vowel_index] + stressed_vowels[token[last_vowel_index]] + token[last_vowel_index + 1:]
        
        return token  # Return unchanged if no stress could be applied
    
    tokens = map(add_stress_if_closed_penult, tokens)
    tokens = map(append_numeric_to_syllable, tokens)
    return tokens

def split_into_syllables(tokens): 
    def split_on_number(token):
        if token in [".", ","]:
            return [token]
        return re.findall(r'\w+?[0-9]', token)  # Use \w+ to include letters and non-ASCII characters

    flattened_list = [syllable for token in tokens for syllable in split_on_number(token)]
    return flattened_list

def convert(input):
    text = normalize(input)
    tokens = split_into_tokens(text)
    tokens = phonemize_exceptions(tokens)
    tokens = match_words_with_dataset(tokens)
    tokens = phonemize_closed_penult(tokens)
    return tokens
