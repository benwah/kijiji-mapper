import json

import requests
import yaml

from bs4 import BeautifulSoup
from jinja2 import Template


SETTINGS = yaml.load(open('secrets.yml', 'r').read())
API_KEY = SETTINGS['geolocation_api_key']
JS_API_KEY = SETTINGS['geolocation_js_api_key']
GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
DEFAULT_PAGES = 10
DEFAULT_URL_TEMPLATE = (
    'http://www.kijiji.ca/b-2-bedroom-apartments-condos/ottawa/{page}c214l1700'
    '185')
DEFAULT_MAP_CENTER = [45.4214, -75.6919]
TEMPLATE_NAME = 'template.jinja2'
FAKE_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like '
    'Gecko) Chrome/40.0.2214.85 Safari/537.36')


def geolocate(address):
    payload = {
        "address": address,
        "key": API_KEY,
    }

    result = requests.get(GOOGLE_MAPS_URL, params=payload)

    result_object = result.json()
    result_results = result_object["results"]
    if len(result_results) < 1:
        return None

    result_geometry = result_results[0]["geometry"]
    latlong = result_geometry["location"]

    return [latlong['lat'], latlong['lng']]


def urls(template, pages):
    yield template.format(page='')

    if pages == 1:
        return

    for page in range(2, pages + 1):
        yield(template.format(page='page-{0}/'.format(page)))


def get_details(url):
    response = requests.get(url, headers={'User-Agent': FAKE_USER_AGENT})
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    details = {
        'price': None,
        'address': None,
        'lat_long': None,
        'date': None,
    }

    price_el = soup.find('span', attrs={'itemprop': 'price'}).find('strong')
    if price_el:
        try:
            details['price'] = float(price_el.text[1:].replace(',', ''))
        except ValueError:
            pass

    address_el = soup.find('th', text='Address').next.next.next
    if address_el:
        details['address'] = address_el.text.split("\n")[0]
        details['lat_long'] = geolocate(details['address'])

    details['date'] = soup.find('th', text='Date Listed').next.next.next.text

    return details


def get_posts(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for item in soup.find_all('table', attrs={'class': 'regular-ad'}):
        title_el = item.find('a', attrs={'class': 'title'})
        title = title_el.text
        link = "http://www.kijiji.ca{path}".format(path=title_el.attrs['href'])
        description = (
            item.find('td', attrs={'class': 'description'}).find('p').text)

        details = get_details(link)

        yield({
            'title': title,
            'link': link,
            'description': description,
            'address': details['address'],
            'price': details['price'],
            'lat_long': details['lat_long'],
            'date': details['date'],
        })


def render_map(appartments):
    with open(TEMPLATE_NAME, 'r') as template_file:
        template = Template(template_file.read())
        return template.render(
            appartments=appartments,
            js_api_key=JS_API_KEY,
            map_center=DEFAULT_MAP_CENTER,
        )


def run():
    template = DEFAULT_URL_TEMPLATE

    appartments = []

    for url in urls(template, DEFAULT_PAGES):
        print("Processing {url}".format(url=url))
        for appartment in get_posts(url):
            appartments.append(appartment)

    the_map = open('map.html', 'w')
    the_map.write(render_map(json.dumps(appartments)))
    the_map.close()


if __name__ == "__main__":
    run()
