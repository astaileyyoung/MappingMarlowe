import re
import pickle
import multiprocessing as mp
from pathlib import Path
from argparse import ArgumentParser

import spacy
import pandas as pd
from tqdm import tqdm
import common
from nlp.Text import Text, Corpus
from Book import Book


def gather_files(d):
    files = [x for x in Path(d).iterdir() if x.suffix in ['.epub', '.mobi', '.pdf']]
    return files


def extract_place_names(text):
    if isinstance(text, str):
        t = Text(text, use_multi=True)
    else:
        t = text
    entities = t.named_entities()
    return entities


def match_places(entities, places):
    matches = []
    for entity in entities:
        for place in places:
            if entity == place:
                matches.append((entity, place))
    return matches


def process_book(fp):
    book = Book(path=fp,
                title=Path(fp).stem)
    book.cleaned = Text(book.text,
                        use_multi=False,
                        lower_case=False)
    return book


def process_books(books):
    processed = []
    for book in tqdm(books):
        processed.append(process_book(book))
    return processed


def process_books_multi(books):
    with mp.Pool() as p:
        processed = list(tqdm(p.imap(process_book, books), total=len(books)))
    return processed


def parse_entities(entities):
    parsed = []
    for entity in entities:
        if entity[1] in ['GPE']:
            parsed.append(entity)
    return parsed


def load_pickle(fp):
    with open(fp, 'rb') as f:
        p = pickle.load(f)
    return p


def load_pickles(fps):
    books = []
    for fp in tqdm(fps):
        b = load_pickle(fp)
        books.append(b)
    return books


def extract_entities(book):
    entities = book.cleaned.named_entities()
    data = [{'word': x[0], 'entity': x[1], 'source': book.title} for x in entities]
    return data


def main(args):
    df = pd.read_csv(args.places, index_col=0)

    files = gather_files(args.dir)
    books = process_books_multi(files)
    c = Corpus(books)

    data = []
    for place in df['name']:
        results = re.findall(place,
                             c.cleaned)
        datum = {'name': place,
                 'count': len(results)}
        data.append(datum)
    temp = pd.DataFrame(data)
    a = 1


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--places', '-p', default='./data/places.csv')
    args = ap.parse_args()
    main(args)
    # df = pd.read_csv(args['places'], index_col=0)
    # entities = extract_place_names(args['book_dir'])
    # df = pd.DataFrame([{'word': x[0], 'entity': x[1]} for x in entities])
    # df.to_csv('data/entities.csv')
    # matches = match_places(entities, list(df['name'].values))
    #
    # with open('data/test.txt', 'r') as f:
    #     text = '\n'.join([x.strip() for x in f.readlines()])
    # nlp = spacy.load('en', parse=True, tag=True, entity=True)
    # text = nlp(text)
    # sentences = [sent.string.strip() for sent in text.sents]
    a = 1
