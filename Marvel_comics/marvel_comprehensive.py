from requests import get
# Requests allows you to send HTTP/1.1 requests extremely easily
import json
from marvel import Marvel
import pandas as pd

df = pd.read_csv('marvel_characters.csv')
for i in df['character_name']:
    url = f'https://gateway.marvel.com:443/v1/public/characters?name={i}&ts=1689856382&apikey=0fee022d3b133b3af21ca3da8d44e242&hash=201976039ad70f0a055f9997b275d578'
    result = get(url)
    print(url)
    json_result = json.loads(result.content)['data']['results']
    comic_value = ''
    if json_result != []:
        comic_items = json_result[0]['comics']['items']
        comic_names = [item["name"] for item in comic_items]
        comic_names.insert(0,i)
        for i in comic_names:
            comic_value = comic_value+i+','
        comic_value = comic_value+'\n'
        with open("marvel_comics.csv", "a") as o:
            o.write(comic_value)
print(comic_value)

