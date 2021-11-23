import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


url = 'https://en.wikipedia.org/wiki/Category:Census-designated_places_in_Los_Angeles_County,_California'
page = requests.get(url)
content = BeautifulSoup(page.content, 'lxml')
temp = content.find_all('div', class_='mw-category')[-1]
eph = temp.find_all('li')
data = []
for i in tqdm(eph):
    p = i.text.split(',')[0]
    try:
        l = 'https://en.wikipedia.org' + i.contents[0]['href']
        next_page = requests.get(l)
        next_content = BeautifulSoup(next_page.content, 'lxml')
        lat_long = next_content.find('a', class_='external text').attrs['href']
    except:
        datum = {'name': p,
                 'latitude': None,
                 'longitude': None}
        data.append(datum)
        continue
    try:
        coord_page = requests.get(lat_long)
    except:
        lat_long = 'http:' + lat_long
        coord_page = requests.get(lat_long)

    coord_content = BeautifulSoup(coord_page.content, 'lxml')
    lat = coord_content.find('span', class_='latitude p-latitude')
    long = coord_content.find('span', class_='longitude p-longitude')
    datum = {'name': p,
             'latitude': lat.text if lat else None,
             'longitude': long.text if long else None}
    data.append(datum)
df = pd.DataFrame(data)
df.to_csv('./data/la_places.csv')

