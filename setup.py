from setuptools import setup, find_packages
import jurispacy_tokenizer

with open("requirements.txt", "r") as file:
    requirements = [l for l in file.read().split("\n") if l and l[:2] != "--"]


setup(
    name="jurispacy-tokenizer",
    version=jurispacy_tokenizer.__version__,
    description="Flair tokenizer adapted to court decisions using spacy tokenization",
    url="https://github.com/Cour-de-cassation/nlp-jurispacy-tokenizer",
    license="MIT License",
    author="Cour de Cassation",
    author_email="amaury.fouret@justice.fr",
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False,
    python_requires=">=3.8",
)
