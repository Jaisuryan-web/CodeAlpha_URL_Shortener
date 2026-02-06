# CodeAlpha URL Shortener

A simple backend URL shortener built using Flask and SQLite as part of the CodeAlpha Backend Development Internship.

## Features
- Generate short URLs
- Redirect short URL to original URL
- REST API based backend
- SQLite database

## Technologies Used
- Python
- Flask
- SQLite

## API Endpoints

### POST /shorten
Creates a short URL.

Request:
```json
{
  "long_url": "https://example.com"
}

#To run the app
install the requirements
python -m pip install -r requirements.txt
python app.py