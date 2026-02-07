# JuriSpacyTokenizer

## Description

Tokenizer(s) used in our NLP projects. Built using [Flair](https://github.com/flairNLP/flair) and [spaCy](https://github.com/explosion/spaCy/)

## Installation

```bash
pip install jurispacy-tokenizer
python -m spacy download fr_core_news_sm-3.8.0
```

## Usage

### Tokenize strings

You can use this library to tokenize a string into a list of strings representing tokens:

```python
from jurispacy_tokenizer import JuriSpacyTokenizer

tokenizer = JuriSpacyTokenizer()
text = "M.Paul et Jean-Pierre sont heureux."

tokens = tokenizer.tokenize(text)

for token in tokens:
    print(token)
```

This should ouptut:

```
M.
Paul
et
Jean-Pierre
sont
heureux
.
```

## Tokenize longer text into sentences

You can also parse longer text to create Flair Sentence objects:

```python
from jurispacy_tokenizer import JuriSpacyTokenizer

tokenizer = JuriSpacyTokenizer()

text = """Bonjour tout le monde! Je m'appelle Amaury.

Je travaille avec Paul."""

sentences = tokenizer.get_tokenized_sentences(text)

for s in sentences:
    print(s)

```

This should output:

```
Sentence[5]: "Bonjour tout le monde!"
Sentence[5]: "Je m'appelle Amaury."
Sentence[5]: "Je travaille avec Paul."
```