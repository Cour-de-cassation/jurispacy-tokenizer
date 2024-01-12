# JuriSpacyTokenizer

## Description

Tokenizer utilisé dans les projets NLP de la Cour de cassation. Il repose sur les librairies [Flair](https://github.com/flairNLP/flair) et [spaCy](https://github.com/explosion/spaCy/).

## Installation

```bash
cd nlp-jurispacy-tokenizer
pip install .
python -m spacy download fr_core_news_sm
```

## Usage

### Tokenization de strings

On peut utiliser cette librairie pour tokenizer des strings en tokens, représentés par des strings.

```python
from jurispacy_tokenizer import JuriSpacyTokenizer

tokenizer = JuriSpacyTokenizer()
text = "M.Paul et Jean-Pierre sont heureux."

tokens = tokenizer.tokenize(text)

for token in tokens:
    print(token)
```

La sortie devrait être:

```
M.
Paul
et
Jean-Pierre
sont
heureux
.
```

## Tokenize de longs textes

On peut aussi utiliser le tokenizer pour récupérer des phrases (`flair.data.Sentence`) à partir de longs textes.

```python
from jurispacy_tokenizer import JuriSpacyTokenizer

tokenizer = JuriSpacyTokenizer()

text = """Bonjour tout le monde! Je m'appelle Amaury.

Je travaille avec Paul."""

sentences = tokenizer.get_tokenized_sentences(text)

for s in sentences:
    print(s)

```

La sortie devrait être:

```
Sentence[5]: "Bonjour tout le monde!"
Sentence[5]: "Je m'appelle Amaury."
Sentence[5]: "Je travaille avec Paul."
```
