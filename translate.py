import requests
import re
import html


class Translator(object):
    """Translation from a source language to a target language using Google Translate."""
    def __init__(self):
        # create a regex for finding the div containing the result of the translation
        # and place it in a named group "translation"
        # (.|\n)* means to match any character including newline, adding ? forces the match to be minimal (ie non-greedy)
        self.regex = re.compile('<div class="result-container">(?P<translation>(.|\n)*?)</div>')

        # base URL of the Google Translate service
        self.base_url = 'https://translate.google.com/m'
        
        # mapping of available languages from/to language codes (eg french <-> fr, russian <-> ru)
        self.code2language = dict(self.get_language_codes())
        self.language2code = {v.lower(): k for k, v in self.code2language.items()}
        
    def get_language_codes(self):
        """Get a list of language names (in English) and their associated language codes."""
        # request page used to choose the source language
        response = requests.get(self.base_url, params={'mui': 'sl', 'hl': 'en'})
        response.raise_for_status()

        # regex to match HTML elements of the form:
        # <div class="language-item"><a href="./m?sl={language_code}&tl&hl=en">{language_name}</a></div>
        regex = re.compile('<div class="language-item"><a href="./m\?sl=(.*?)\&.*?">(.*?)</a></div>')

        # find and return all matches
        matches = regex.findall(html.unescape(response.text))
        return matches

    def translate(self, text, tl, sl='auto'):
        """Translate a text from a source language to a target language."""
        # make sure source and target languages are supported
        source_language = sl.lower()
        target_language = tl.lower()

        if source_language != 'auto':
            if source_language not in self.code2language:
                if source_language not in self.language2code:
                    raise ValueError(f'Source language {source_language} is not supported.')
                source_language = self.language2code[source_language]

        if target_language not in self.code2language:
            if target_language not in self.language2code:
                raise ValueError(f'Target language {target_language} is not supported.')
            target_language = self.language2code[target_language]

        # create params for the GET request
        params = {
            'sl': source_language,
            'tl': target_language,
            'q': text,
        }

        # make request
        response = requests.get(self.base_url, params=params, timeout=5.0)

        # raise an exception if status code is not 200
        response.raise_for_status()

        # return translated text
        match = self.regex.search(html.unescape(response.text))
        translation = match.group('translation')
        return translation
