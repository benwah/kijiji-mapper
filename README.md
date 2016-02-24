# KIJIJI MAPPER

Outputs a map of places from Kijiji by scraping its HTML and making calls to Google geo-location API.

## Setup:

* Git clone
* Install dependencies: python setup.py develop
* Go here: https://console.developers.google.com, create a project and enable google APIs:
  * Google Maps Geocoding API
  * Google Maps JavaScript API
* Get your credentials from Google API Coneole. (API Keys, "Server" and "Browser" key)
* Copy those to secrets.yml, see secrets.yml.example to get an example.
* Edit run.py. Things you might need to change:
  * DEFAULT_PAGES (how many pages to crawl?)
  * DEFAULT_URL_TEMPLATE
    * Defaults to: http://www.kijiji.ca/b-2-bedroom-apartments-condos/ottawa/{page}c214l1700185
    * Just browse on Kijiji, when you find a category you like, copy the URL. Make sure to inser the {page} formatting token on the URL at the appropriate spot!
