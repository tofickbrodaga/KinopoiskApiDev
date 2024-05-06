from os import getenv

HEADERS = {
        "accept": "application/json",
        "X-API-KEY": getenv('API_KEY')
    }

#http codes
OK = 200
MOVED = 302

#methods
POST = 'POST'
GET = 'GET'