import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
from prodigy.util import split_string
import spacy
from typing import List, Optional
import re  # Import regular expressions

def get_core_terms():
    with open('./data/coreterm2.txt', 'r') as fp:
        line = fp.readline()
        core =[]
        while line:
            c = line.split()
            core.append(c[0])
            line = fp.readline()
    return core

core = get_core_terms()
#print(len(core))

# Recipe decorator with argument annotations: (description, argument type,
# shortcut, type / converter function called on value before it's passed to
# the function). Descriptions are also shown when typing --help.
@prodigy.recipe(
    "ner.my_recipe1",
    dataset=("The dataset to use", "positional", None, str),
    spacy_model=("The base model", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    label=("One or more comma-separated labels", "option", "l", split_string),
    exclude=("Names of datasets to exclude", "option", "e", split_string),
    highlight_chars=("Allow highlighting individual characters instead of tokens", "flag", "C", bool),
)
def ner_manual(
    dataset: str,
    spacy_model: str,
    source: str,
    label: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    highlight_chars: bool = False,
):
    """
    Mark spans manually by token. Requires only a tokenizer and no entity
    recognizer, and doesn't do any active learning.
    """
    # Load the spaCy model for tokenization
    nlp = spacy.load(spacy_model)

    # Load the stream from a JSONL file and return a generator that yields a
    # dictionary for each example in the data.
    stream = JSONL(source)
    stream = add_core_character_spans(stream)

    #print(next(stream))
    #print(dir(stream))

    # Tokenize the incoming examples and add a "tokens" property to each
    # example. Also handles pre-defined selected spans. Tokenization allows
    # faster highlighting, because the selection can "snap" to token boundaries.
    stream = add_tokens(nlp, stream)

    stream = add_tokens(nlp, stream, use_chars=highlight_chars)

    return {
        "view_id": "ner_manual",  # Annotation interface to use
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "exclude": exclude,  # List of dataset names to exclude
        "config": {  # Additional config settings, mostly for app UI
            "lang": nlp.lang,
            "labels": label,  # Selectable label options
        },
    }

def strip_spaces(text):
    # strip whitespaces of the begining and the end of the text
    text.strip(' ')

    # use regular expression to eliminate more than 1 whitespaces to only 1 whitespace in the middle of the text
    text = re.sub(" +", " ", text)
    return text

def get_spans(title):
    text = title['text']
    text = strip_spaces(text)
    title['text'] = text

    for term in core:
        start = text.find(term)
        if start != -1:
            break

    if start != -1:
        end = start + len(term)
        spans = dict()
        spans['start'] = start
        spans['end'] = end
        spans['label'] = 'CORE'

        # whitespace can't be a token
        tokenized_text = text.replace(' ', '')

        token_start = tokenized_text.find(term)
        token_end = token_start + len(term) - 1
        spans['token_start'] = token_start
        spans['token_end'] = token_end

        title["spans"] = [spans]
    return title


def add_core_character_spans(stream):
    s = (get_spans(title) for title in stream)
    return s