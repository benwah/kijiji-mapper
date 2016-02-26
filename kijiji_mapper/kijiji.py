import requests
from bs4 import BeautifulSoup

from kijiji_mapper.geo import geolocate


def urls(template, pages):
    yield template.format(page='')

    if pages == 1:
        return

    for page in range(2, pages + 1):
        yield(template.format(page='page-{0}/'.format(page)))


def get_details(url, user_agent):
    response = requests.get(url, headers={'User-Agent': user_agent})
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


def get_posts(url, user_agent):
    response = requests.get(url, headers={'User-Agent': user_agent})
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for item in soup.find_all('table', attrs={'class': 'regular-ad'}):
        title_el = item.find('a', attrs={'class': 'title'})
        title = title_el.text
        link = "http://www.kijiji.ca{path}".format(path=title_el.attrs['href'])
        description = (
            item.find('td', attrs={'class': 'description'}).find('p').text)

        details = get_details(link, user_agent)

        yield({
            'title': title,
            'link': link,
            'description': description,
            'address': details['address'],
            'price': details['price'],
            'lat_long': details['lat_long'],
            'date': details['date'],
        })


def yield_posts(url_template, pages, user_agent):
    for url in urls(url_template, pages):
        print("Processing {url}".format(url=url))
        for appartment in get_posts(url, user_agent):
            yield(appartment)
