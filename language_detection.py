
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import spacy

class LanguageDetection:
    def __init__(self):
        self._nlp = self.load_nlp()

    @Language.factory("language_detector")
    def get_lang_detector(nlp, name):
        return LanguageDetector()

    def detect_lang(self, text):
        return self._nlp(text)._.language["language"]

    @staticmethod
    def load_nlp() -> Language:
        nlp = spacy.load("en_core_web_lg")
        nlp.add_pipe("language_detector", last=True)
        return nlp
