# JuriSpacyTokenizer

## Description

Tokenizer(s) used in our NLP projects. Built using [Flair](https://github.com/flairNLP/flair) and [spaCy](https://github.com/explosion/spaCy/)

## Installation

```bash
cd nlp-jurispacy-tokenizer
pip install .
python -m spacy download fr_core_news_sm
```

## Usage

```python
from jurispacy_tokenizer import JuriSpacyTokenizer
from flair.data import Sentence

tokenizer = JuriSpacyTokenizer()
sent = Sentence("M.Paul et Jean-Pierre sont heureux.", use_tokenizer=tokenizer)
for token in sent:
    print(token)
```
