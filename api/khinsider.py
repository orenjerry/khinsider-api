import requests
from bs4 import BeautifulSoup
from flask import Blueprint
from flask_restful import Api, Resource

def scrape_khinsider_albums():
    url = "https://downloads.khinsider.com/game-soundtracks"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='albumList')
        albums = []

        for row in table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) == 5:
                img_tag = columns[0].find('img')
                album_url = 'https://downloads.khinsider.com' + columns[1].find('a')['href']
                album_id = album_url.split('/album/', 1)[-1] if '/album/' in album_url else None
                album = {
                    'id': album_id,
                    'image_url': img_tag['src'] if img_tag else None,
                    'album_url': album_url,
                    'album_name': columns[1].text.strip(),
                    'platform': columns[2].text.strip() if columns[2] else None,
                    'type': columns[3].text.strip() if columns[3] else None,
                    'year': columns[4].text.strip() if columns[4] else None
                }
                albums.append(album)

        return {"status": "200", "message": "Received albums", "data": {"albums": albums}}, 200
    else:
        return {"status": "400", "message": "Failed to receive albums"}, 400

class get_khinsider_albums(Resource):
    def get(self):
        albums, status_code = scrape_khinsider_albums()
        return albums, status_code

data_blueprint = Blueprint('data', __name__)
data = Api(data_blueprint)
data.add_resource(get_khinsider_albums, '/khinsider/albums')