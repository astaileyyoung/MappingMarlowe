import pickle
import traceback

from bs4 import BeautifulSoup, NavigableString
from ebooklib import epub


class Book(object):
    def __init__(self, path=None, title=None, author=None, publisher=None, year=None, epub=None, text=None, cleaned=None):
        self.path = path
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.epub = epub
        self.text = text
        self.cleaned = cleaned

        if self.path:
            self.load_epub(self.path)

    def load_epub(self, path):
        self.epub = epub.read_epub(path)
        contents = self.epub.get_items()
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

        self.text = ' '.join(t)


if __name__ == '__main__':
    b = Book('sources/big_sleep.epub')
    a = 1
