import re
import logging

from flair.data import Tokenizer, Sentence

from .config import SPECIAL_CASES

__version__ = "1.1.6"


class JuriSpacyTokenizer(Tokenizer):
    """
    Implementation of :class:`Tokenizer`, using French model from Spacy.
    """

    def __init__(self):
        super(JuriSpacyTokenizer, self).__init__()

        try:
            import spacy
            from spacy.attrs import ORTH
        except ImportError as e:
            raise ImportError(
                "Please install Spacy v2.0 or better before using the Spacy tokenizer, "
                "otherwise you can use SegtokTokenizer as advanced tokenizer."
            ) from e

        self.spacy_version = spacy.__version__
        self.nlp = spacy.load(
            "fr_core_news_sm",
            exclude=["tok2vec", "morphologizer", "parser", "senter", "attribute_ruler", "lemmatizer", "ner"],
        )
        # Attribute max_length raise a ValueError
        # if number of characters exceed the default value
        self.nlp.max_length = 1000000000

        # Add special cases
        for c in SPECIAL_CASES:
            case = [{ORTH: c}]
            self.nlp.tokenizer.add_special_case(c, case)

        # Silencing flair EmptySentence warnings
        flair_logger = logging.getLogger("flair")
        flair_logger.addFilter(EmptySentenceWarningFilter)

    def tokenize(self, text: str) -> list[str]:
        """Tokenizes a text into a list of tokens as strings.

        Args:
            text (str): text to tokenize.

        Returns:
            list[str]: list of tokens as string.
        """
        from spacy.tokens.doc import Doc

        doc: Doc = self.nlp(text)
        words: list[str] = []

        # Handle case like M.Dupont : split into 2 tokens (M., Dupont)
        # like_typo_mister = re.compile(r"M(?:M|r?)\.(?:[A-Z]\w+)")
        # Handle case missing space between tél and number
        # like_typo_phone = re.compile(r"t(?:é|e)l\.(?:([0-9]+)$)")
        # Both in one regex
        like_mister_phone = re.compile(r"M(?:M|r?)\.(?:[A-Z]\w+)|t(?:é|e)l\.(?:([0-9]+)$)")
        # Handle case like "[M. Dupont]." :
        # split  the token "Dupont]." into three tokens : "Dupont", "]" and "."
        like_square_bracket_dot = re.compile(r"\S+]\.")
        for i, tok in enumerate(doc):
            if re.match(like_square_bracket_dot, tok.text):
                split_toks = tok.text.split("]", 1)
                tok1 = split_toks[0]
                tok2 = "]"
                tok3 = split_toks[1]
                heads = [(doc[i], 1), (doc[i], 0), (doc[i], 0)]
                with doc.retokenize() as retokenizer:
                    retokenizer.split(doc[i], [tok1, tok2, tok3], heads=heads)

            if re.match(like_mister_phone, tok.text):
                split_toks = tok.text.split(".", 1)
                tok1, tok2 = f"{split_toks[0]}.", split_toks[1]
                heads = [(doc[i], 1), (doc[i], 0)]
                with doc.retokenize() as retokenizer:
                    retokenizer.split(doc[i], [tok1, tok2], heads=heads)

            # Handle case like "-Dupont" :
            # split  the token "-Dupont" into two tokens : "-" and "Dupont"
            if tok.text.startswith("-") and len(tok.text) > 1 and tok.text[1].isupper():
                split_toks = tok.text.split("-", 1)
                tok1, tok2 = "-", split_toks[1]
                heads = [(doc[i], 1), (doc[i], 0)]
                with doc.retokenize() as retokenizer:
                    retokenizer.split(doc[i], [tok1, tok2], heads=heads)

        # Handle case like Jean-Paul : keep only one token for hyphenated name
        like_hyphenated_name = re.compile(r"(?:[A-Z][a-zA-Z]+)-(?:[A-Z][a-zA-Z]+)")
        if re.search(like_hyphenated_name, doc.text):
            for match in re.finditer(like_hyphenated_name, doc.text):
                if token_idx := [token.i for token in doc if match.start() <= token.idx < match.end()]:
                    with doc.retokenize() as retokenizer:
                        retokenizer.merge(doc[token_idx[0] : token_idx[-1] + 1])

        words.extend(word.text for word in doc if len(word.text.strip()) != 0 or "\n" in word.text)

        return words

    def get_tokenized_sentences(self, text: str) -> list[Sentence]:
        """Method that returns a list of flair.data.Sentence from a long text
        Args:
            text (str): test to split into tokenized sentences
        Returns:
            list[Sentence]: a list of Sentences
        """
        sentences = []
        s_tokens = []
        s = Sentence("")

        tokenized_text = Sentence(text, self)
        n_tokens = len(tokenized_text)

        for index_token, token in enumerate(tokenized_text):
            if (index_token == n_tokens - 1) and (not token.text.isspace()):
                token.sentence = None
                s_tokens.append(token)
                s = Sentence(
                    s_tokens,
                    use_tokenizer=False,
                    start_position=s_tokens[0].start_position,
                )
                sentences.append(s)
                s_tokens = []
            elif (not token.text.isspace()) and (token.text not in ["?", ".", "!", ";"]):
                token.sentence = None
                s_tokens.append(token)
            elif token.text in ["?", ".", "!", ";"]:
                token.sentence = None
                s_tokens.append(token)
                s = Sentence(
                    s_tokens,
                    use_tokenizer=False,
                    start_position=s_tokens[0].start_position,
                )
                s_tokens = []
                sentences.append(s)
            elif "\n" in token.text:
                if len(s_tokens) > 0:
                    s = Sentence(
                        s_tokens,
                        use_tokenizer=False,
                        start_position=s_tokens[0].start_position,
                    )
                    sentences.append(s)
                    s_tokens = []
        return [s for s in sentences if len(s) > 0]

    @property
    def name(self) -> str:
        """Returns the name and version of JuriSpacyTokenizer"""
        return f"JuriSpacyTokenizer_v{__version__}_using_spacy_v.{self.spacy_version}"


class EmptySentenceWarningFilter(logging.Filter):
    """Logging filter to prevent empty Sentence Warnings from flair"""

    def filter(self, record=None):
        """Returns True if 'empty Sentence' is not in record"""
        return record and "empty Sentence" not in record.getMessage()
