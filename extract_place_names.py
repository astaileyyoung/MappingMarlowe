import traceback
from pathlib import Path
from argparse import ArgumentParser

import spacy
import pandas as pd
from tqdm import tqdm
from ebooklib import epub
from bs4 import BeautifulSoup, NavigableString


class Place(object):
    def __init__(self, name, state=None, city=None, county=None, country=None, latitude=None, longitude=None):
        self.name = name
        self.state = state
        self.city = city
        self.county = county
        self.country = country
        self.latitude = latitude
        self.longitude = longitude


def gather_files(d):
    files = [x for x in Path(d).iterdir() if x.suffix in ['.epub', '.mobi', '.pdf']]
    return files


def load_epub(path):
    e = epub.read_epub(path)
    contents = e.get_items()
    xmls = [x.get_content() for x in contents]
    texts = [BeautifulSoup(x.decode('utf-8', 'replace'), 'xml') for x in xmls]
    t = []
    for text in texts:
        temp = text.find_all('p')
        content = []
        for x in temp:
            try:
                if 'class' in x.attrs.keys():
                    if x.attrs['class'] in ['tx', 'cotx1', 'indent', 'nonindent'] and isinstance(x.contents[0], NavigableString):
                        content.append(x.contents[0])
                else:
                    if isinstance(x.contents[0], str) or isinstance(x.contents[0], NavigableString):
                        content.append(x.contents[0])

            except:
                traceback.print_exc()
        [t.append(x) for x in content]

    return ' '.join(t)


def main(args):
    nlp = spacy.load('xx_ent_wiki_sm')

    files = gather_files(args.src)
    data = []
    for file in tqdm(files):
        text = load_epub(str(file))
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                datum = {'name': ent.text,
                         'entity': ent.label_,
                         'source': str(file)}
                data.append(datum)
    df = pd.DataFrame(data)
    df.to_csv()


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    args = ap.parse_args()
    main(args)
