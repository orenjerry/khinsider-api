# KHInsider Scraper API

This project is a Flask-based API that scrapes video game soundtrack information from KHInsider, a popular video game music website. It provides endpoints to retrieve album listings, album details, and individual song download URLs.

## Features

- Retrieve the latest album listings from KHInsider's home page
- Get detailed information about a specific album
- Fetch download URLs for individual songs

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/orenjerry/khinsider-scraper-api.git
   cd khinsider-scraper-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. The API will be available at `http://localhost:8001`. You can use the following endpoints:

   - GET `/api/khinsider`: Retrieve the latest album listings
   - GET `/api/khinsider/album/<album_id>`: Get detailed information about a specific album
   - GET `/api/khinsider/album/<album_id>/<song_id>`: Fetch the download URL for a specific song

## API Endpoints

### Get Latest Albums
```bash
GET /api/khinsider
```
Returns a list of the latest albums from KHInsider's home page.

### Get Album Details
```bash
GET /api/khinsider/album/<album_id>
```
Returns detailed information about a specific album.

### Get Song Download URL
```bash
GET /api/khinsider/album/<album_id>/<song_id>
```
Returns the download URL for a specific song.

## Error Handling

The API includes error handling and logging. If an error occurs, it will be logged in the `error.log` file.

## Disclaimer

This project is for educational purposes only. Please respect KHInsider's terms of service and use this API responsibly.

## License

[MIT License](LICENSE)
