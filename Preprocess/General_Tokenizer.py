import unicodedata
from hazm import Stemmer


class General_Tokenizer:
    stemmer = Stemmer()
    punctuation_mapping = {char: ' ' for char in 'ء؛!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~،><«»؟'}
    diacritic_mapping = {
        # Diacritic marks
        '\u064B': '',  # Fathatan
        '\u064C': '',  # Dammatan
        '\u064D': '',  # Kasratan
        '\u064E': '',  # Fatha
        '\u064F': '',  # Damma
        '\u0650': '',  # Kasra
        '\u0651': '',  # Shadda
        '\u0652': '',  # Sukun
        '\u0653': '',  # Maddah above
        '\u0654': '',  # Hamza above
        '\u0655': '',  # Hamza below
        'أ': 'ا',
        'ة': 'ه'
    }
    number_mapping = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }
    half_space_mapping = {
        'می ': 'می\u200c',
        'نمی ': 'نمی\u200c'
    }

    def process(self, text):
        text = text.lower()

        text = text.translate(str.maketrans(self.punctuation_mapping))

        cleaned_text = ''
        for char in text:
            # Check if the character is an Arabic character with a diacritic mark
            if unicodedata.category(char) == 'Mn' and char in self.diacritic_mapping:
                # Remove the diacritic mark
                cleaned_text += self.diacritic_mapping[char]
            else:
                # Add the character as is
                cleaned_text += char

        cleaned_text = cleaned_text.translate(str.maketrans(self.number_mapping))
        cleaned_text = cleaned_text.translate(str.maketrans(self.half_space_mapping))

        tokens = cleaned_text.split()

        position = 1
        local_positions = {}
        for token in tokens:
            token = self.stemmer.stem(token)
            token_positions = local_positions.get(token)
            if token_positions is None:
                local_positions[token] = [position]
            else:
                token_positions.append(position)
            position += 1

        return local_positions
