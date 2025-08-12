import re
from collections import Counter


class TextAnalyzer:
    """
    A utility class for performing various text analyses.
    """

    def __init__(self, text: str):
        self.text = text

    def word_count(self) -> int:
        return len(self.text.split())

    def char_count(self) -> int:
        return len(self.text)

    def unique_words(self) -> int:
        return len(set(word.lower() for word in self.text.split()))

    def line_count(self) -> int:
        return len(self.text.splitlines())

    def sentence_count(self) -> int:
        sentences = re.split(r'[.!?]+', self.text)
        return len([s for s in sentences if s.strip()])

    def most_common_word(self) -> str:
        words = [w.lower() for w in re.findall(r'\b\w+\b', self.text)]
        if not words:
            return ""
        return Counter(words).most_common(1)[0][0]

    def vowel_count(self) -> int:
        return sum(ch in "aeiouAEIOU" for ch in self.text)

    def digit_count(self) -> int:
        return sum(ch.isdigit() for ch in self.text)

    def special_char_count(self) -> int:
        return sum(not ch.isalnum() and not ch.isspace() for ch in self.text)

    def analyze(self, analyses: list[str]) -> dict:
        """
        Perform selected analyses on the input text.

        Supported analyses:
        - word_count
        - char_count
        - unique_words
        - line_count
        - sentence_count
        - most_common_word
        - vowel_count
        - digit_count
        - special_char_count

        Args:
            analyses (list[str]): List of analyses to perform.

        Raises:
            Exception: If unsupported analysis is requested.

        Returns:
            dict: Dictionary with analysis results.
        """
        supported = {
            "word_count": self.word_count,
            "char_count": self.char_count,
            "unique_words": self.unique_words,
            "line_count": self.line_count,
            "sentence_count": self.sentence_count,
            "most_common_word": self.most_common_word,
            "vowel_count": self.vowel_count,
            "digit_count": self.digit_count,
            "special_char_count": self.special_char_count,
        }

        result = {}
        for analysis in analyses:
            if analysis not in supported:
                raise Exception(f"Unsupported analysis type: '{analysis}'")
            result[analysis] = supported[analysis]()

        return {"results": result}
