import spacy
import pandas as pd

from nlp.Text import Text
from Book import Book


a = pd.read_csv('data/places.csv', index_col=0)
b = pd.read_csv('./data/la_places.csv', index_col=0)

a = a[~a['name'].isin(b['name'])]

df = pd.concat([a, b])
df.to_csv('./data/places.csv')
a = 1
# with open('data/test.txt', 'r') as f:
#     text = f.read()
# path = '/home/amos/programs/MappingMarlowe/marlowe/sources/playback.epub'
# b = Book(path)
#
# t = Text(b.text)
# nlp = spacy.load('en')
# c = nlp(t.cleaned)
# e = [x for x in c.ents if x.label_ == 'GEO']
# entities = t.named_entities()
# [print(x) for x in entities]


