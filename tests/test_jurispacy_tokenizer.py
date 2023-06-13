import pytest
from flair.data import Sentence
from jurispacy_tokenizer import JuriSpacyTokenizer

tokenizer = JuriSpacyTokenizer()


def test_mister_with_no_space():
    sent = Sentence("M. Fouret et M.Barrière.", use_tokenizer=tokenizer)
    assert len(sent) == 6
    assert sent[3].text == "M."
    assert sent[4].text == "Barrière"


def test_hyphanted_names():
    sent = Sentence(
        "Jean-Pierre et Marie-Claude mangent ensemble.", use_tokenizer=tokenizer
    )
    assert len(sent) == 6
    assert sent[0].text == "Jean-Pierre"
    assert sent[2].text == "Marie-Claude"


def test_square_bracket_dot():
    sent = Sentence("[M. Dupont].", use_tokenizer=tokenizer)
    assert len(sent) == 5
    assert sent[2].text == "Dupont"
    assert sent[3].text == "]"
    assert sent[4].text == "."


def test_get_tokenized_sentences():
    text = """Bonjour tout le monde!

    On va dire des choses simples. Le chat de Paul est plus mignon, voir bien plus mignon, que le chien d'Amaury.
    Ch. Criminelle de la cour de récré de Paris
    """

    computed_sentences = tokenizer.get_tokenized_sentences(text=text)

    assert len(computed_sentences) == 4

    assert len(computed_sentences[0]) == 5, [t.text for t in computed_sentences[0]]
    assert len(computed_sentences[1]) == 7, [t.text for t in computed_sentences[1]]
    assert len(computed_sentences[2]) == 19, [t.text for t in computed_sentences[2]]
    assert len(computed_sentences[3]) == 9, [t.text for t in computed_sentences[3]]
