import re

import unicodedata
from hazm import Stemmer


class General_Tokenizer:
    stemmer = Stemmer()
    punctuation_mapping = {char: ' ' for char in 'ء؛!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~،><«»؟《》⁩“'}
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

    polymorphism_words = {
        "﷽": "بسم الله الرحمن الرحیم",
        "﷼": "ریال",
        "ﷹ": "صلی",
        "ﷰ": "صلی",
        "ﷲ": "الله",
        "ﷳ": "اکبر",
        "ﷴ": "محمد",
        "ﷵ": "صلعم",
        "ﷶ": "رسول",
        "ﷷ": "علیه",
        "ﷸ": "وسلم",
        "ﻼ": "لا",
        "ﻻ": "لا",
        "ﻺ": "لا",
        "ﻹ": "لا",
        "ﻸ": "لا",
        "ﻷ": "لا",
        "ﻶ": "لا",
        "ﻵ": "لا",
        'کتاب خانه': 'کتابخانه',
        'گفت و گو': 'گفتگو',
        'جست و جو': 'جستجو',
        'قران': 'قرآن',
        'شست و شو': 'شستشو',
        'مهمان سرا': 'مهمانسرا',
        'ایران خودرو': 'ایرانخودرو'
    }
    alphabet_convert = {
        "آ": "آ",
        "ﺁ": "آ",
        "ك": "ک",
        "ڪ": "ک",
        "ﮐ": "ک",
        "ﮑ": "ک",
        "ﻛ": "ک",
        "ګ": "ک",
        "ﮏ": "ک",
        "ﻜ": "ک",
        "ﮎ": "ک",
        "ﻚ": "ک",
        "ڭ": "ک",
        "ي": "ی",
        "ى": "ی",
        "ے": "ی",
        "ێ": "ی",
        "ﯿ": "ی",
        "ﯾ": "ی",
        "ﯽ": "ی",
        "ې": "ی",
        "ﯼ": "ی",
        "ﻴ": "ی",
        "ﻳ": "ی",
        "ں": "ی",
        "ﻲ": "ی",
        "ﻱ": "ی",
        "ﻰ": "ی",
        "ۍ": "ی",
        "ﻯ": "ی",
        "ﭛ": "ی",
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

        # Using regex to add spaces before and after numbers
        cleaned_text = re.sub(r'(\d+)', r' \1 ', cleaned_text)

        for x in self.half_space_mapping.keys():
            cleaned_text.replace(x, self.half_space_mapping.get(x))
        for x in self.polymorphism_words.keys():
            cleaned_text.replace(x, self.polymorphism_words.get(x))
        for x in self.alphabet_convert.keys():
            cleaned_text.replace(x, self.alphabet_convert.get(x))

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
