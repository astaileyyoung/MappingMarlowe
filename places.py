import re

from pathlib import Path
from collections import Counter
from argparse import ArgumentParser

import spacy
import pandas as pd
from tqdm import tqdm

from nlp.utils import load_epub


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


def get_places(src,
               model='en_core_web_sm',
               ):
    nlp = spacy.load(model)

    data = []
    text = load_epub(src)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            datum = {'name': ent.text,
                     'entity': ent.label_,
                     'source': src}
            data.append(datum)
    df = pd.DataFrame(data)
    return df


def parse_places(df,
                 places_path='./data/places.csv'):
    names = list(set(df['name'].values))
    places = pd.read_csv(places_path, index_col=0)

    # locations = df[df['entity'] == 'GPE']
    # c = Counter(locations['name'])
    # locations = pd.DataFrame([{'name': k,
    #                            'count': v,
    #                            'source': src} for k, v in c.items()])
    data = []
    for name in names:
        locations = places[places['name'].str.contains(fr'^{name}\Z',
                                                       flags=re.IGNORECASE)]
        if locations.shape[0] > 0:
            lat = locations.iloc[0]['latitude']
            long = locations.iloc[0]['longitude']
            temp = df[df['name'] == name]
            datum = {'name': name,
                     'count': temp.shape[0],
                     'latitude': lat,
                     'longitude': long}
            data.append(datum)
    parsed = pd.DataFrame(data)
    return parsed


def main(args):
    if Path(args.src).is_dir():
        files = gather_files(args.src)

        dfs = []
        for file in tqdm(files):
            df = get_places(str(file),
                            model=args.model)
            dfs.append(df)
        total = pd.concat(dfs)
        total.reset_index(inplace=True)
        total.to_csv('./data/corpus_places.csv')
    else:
        total = pd.read_csv(args.src, index_col=0)

    parsed = parse_places(total,
                          places_path=args.places)
    parsed.to_csv(args.dst)


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--model', '-m', default='en_core_web_sm', type=str)
    ap.add_argument('--places', '-p', default='./data/places.csv', type=str)
    args = ap.parse_args()
    main(args)
