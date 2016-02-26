import yaml


settings = yaml.load(open('secrets.yml', 'r').read())

# API_KEY = SETTINGS['geolocation_api_key']
# JS_API_KEY = SETTINGS['geolocation_js_api_key']
# GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
# DEFAULT_PAGES = 1
# DEFAULT_URL_TEMPLATE = (
#     'http://www.kijiji.ca/b-2-bedroom-apartments-condos/ottawa/{page}c214l1700'
#     '185')
# DEFAULT_MAP_CENTER = [45.4214, -75.6919]
# TEMPLATE_NAME = 'template.jinja2'
# FAKE_USER_AGENT = (
#     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like '
#     'Gecko) Chrome/40.0.2214.85 Safari/537.36')
