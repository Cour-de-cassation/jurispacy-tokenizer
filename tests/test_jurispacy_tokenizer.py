import pytest
from flair.data import Sentence
from jurispacy_tokenizer import JuriSpacyTokenizer

tokenizer = JuriSpacyTokenizer()


def test_names_without_space():
    sent = Sentence(
        "M. Fouret et M.Barrière MmeBIDULE etDUPONT MACHINfaisant alorsTRUCmuche BIDULEMadame É.Chouette MONSIEURPendule MMme ROND.",
        use_tokenizer=tokenizer,
    )
    print(sent.tokens)
    assert len(sent) == 21
    assert sent[3].text == "M."
    assert sent[4].text == "Barrière"
    assert sent[5].text == "Mme"
    assert sent[6].text == "BIDULE"
    assert sent[7].text == "et"
    assert sent[8].text == "DUPONT"
    assert sent[9].text == "MACHIN"
    assert sent[10].text == "faisant"
    assert sent[11].text == "alorsTRUCmuche"
    assert sent[12].text == "BIDULE"
    assert sent[13].text == "Madame"
    assert sent[14].text == "É."
    assert sent[15].text == "Chouette"
    assert sent[16].text == "MONSIEUR"
    assert sent[17].text == "Pendule"
    assert sent[18].text == "MMme"


def test_hyphenated_names():
    sent = Sentence(
        "Jean-Pierre et Marie-Claude ainsi qu'Aimé-Charles mangent ensemble -Esc1-RDC- Bat A.",
        use_tokenizer=tokenizer,
    )
    assert len(sent) == 12
    assert sent[0].text == "Jean-Pierre"
    assert sent[2].text == "Marie-Claude"
    assert sent[5].text == "Aimé-Charles"


def test_square_bracket_dot():
    sent = Sentence("[M. Dupont].", use_tokenizer=tokenizer)
    assert len(sent) == 5
    assert sent[2].text == "Dupont"
    assert sent[3].text == "]"
    assert sent[4].text == "."


def test_token_starts_with_hyphen():
    sent = Sentence("-Amaury est né ici.", use_tokenizer=tokenizer)
    assert len(sent) == 6
    assert sent[0].text == "-"
    assert sent[1].text == "Amaury"


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
