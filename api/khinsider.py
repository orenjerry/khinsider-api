import requests
from bs4 import BeautifulSoup
from flask import Blueprint
from flask_restful import Api, Resource
from datetime import datetime
def scrape_khinsider_home():
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

        return {"status": "200", "message": "Received khinsider home", "data": {"albums": albums}}, 200
    else:
        return {"status": "400", "message": "Failed to receive khinsider home"}, 400
    
def scrape_khinsider_album(album_id):
    try:
        url = f"https://downloads.khinsider.com/game-soundtracks/album/{album_id}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            page = soup.find('div', id='pageContent')
            title = page.find('h2').text.strip()
            title_alt = page.find('p', class_='albuminfoAlternativeTitles').text.strip()
            
            left_align = page.find('p', align='left')
            year = left_align.find('b', text=True).text.strip()
            
            developers = [a.text.strip() for a in left_align.find_all('a', href=lambda x: x and '/game-soundtracks/developer/' in x)]
            publishers = [a.text.strip() for a in left_align.find_all('a', href=lambda x: x and '/game-soundtracks/publisher/' in x)]
            
            if developers:
                developers = developers if len(developers) > 1 else developers[0]
            else:
                developers = None
            
            if publishers:
                publishers = publishers if len(publishers) > 1 else publishers[0]
            else:
                publishers = None
            
            if len(left_align.find_all('b')) == 5:
                num_files = left_align.find_all('b')[1].text.strip()
                date_added = left_align.find_all('b')[3].text.strip()
            else:
                num_files = left_align.find_all('b')[2].text.strip()
                date_added = left_align.find_all('b')[5].text.strip() if len(left_align.find_all('b')) > 6 else left_align.find_all('b')[4].text.strip()
            uploaders = [a.text.strip() for a in left_align.find_all('a', href=lambda x: x and '/forums/index.php?members/' in x)]
            
            album_images = []
            album_image_divs = page.find_all('div', class_='albumImage')
            for div in album_image_divs:
                img_tag = div.find('img')
                if img_tag:
                    album_images.append({
                        'thumbnail': img_tag['src'],
                        'full_size': div.find('a')['href']
                    })

            table = page.find('table', id='songlist')
            songs = []

            if table:
                for row in table.find_all('tr')[1:-1]:  # Skip the header row and footer row
                    columns = row.find_all('td')
                    if len(columns) == 9:
                        song = {
                            'cd': columns[1].text.strip(),
                            'track': columns[2].text.strip(),
                            'song_name': columns[3].text.strip(),
                            'length': columns[4].text.strip(),
                        }
                    elif len(columns) == 8:
                        song = {
                            'track': columns[1].text.strip(),
                            'song_name': columns[2].text.strip(),
                            'length': columns[3].text.strip(),
                        }
                    elif len(columns) == 7:
                        song = {
                            'track': columns[1].text.strip(),
                            'song_name': columns[2].text.strip(),
                            'length': columns[3].text.strip(),
                        }
                    elif len(columns) == 6:
                        song = {
                            'song_name': columns[1].text.strip(),
                            'length': columns[2].text.strip(),
                        }
                    songs.append(song)
                return {
                    "status": "200", 
                    "message": "Received khinsider album", 
                    "data": {
                        "title": title,
                        "alternative_title": title_alt,
                        "album_images": album_images,
                        "release_year": year,
                        "developers": developers,
                        "publisher": publishers,
                        "total_files": num_files,
                        "date_added": date_added,
                        "uploaders": uploaders,
                        "songs": songs
                    }
                }, 200
            else:
                return {"status": "404", "message": "Album not found or has no song list"}, 404
        else:
            return {"status": "400", "message": "Failed to receive khinsider album"}, 400
    except Exception as e:
        with open('error.log', 'a') as error_file:
            error_file.write(f"{datetime.now()}:\n Error in scrape_khinsider_album with album_id: {album_id}\n Error message: {str(e)}\n\n")
        return {"status": "500", "message": "There's an error, the error has been reported to the developers"}, 500

class get_khinsider_home(Resource):
    def get(self):
        albums, status_code = scrape_khinsider_home()
        return albums, status_code
    
class get_khinsider_album(Resource):
    def get(self, album_id):
        album, status_code = scrape_khinsider_album(album_id)
        return album, status_code

data_blueprint = Blueprint('data', __name__)
data = Api(data_blueprint)
data.add_resource(get_khinsider_home, '/khinsider/')
data.add_resource(get_khinsider_album, '/khinsider/album/<string:album_id>')