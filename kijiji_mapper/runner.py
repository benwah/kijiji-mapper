from kijiji_mapper.kijiji import yield_posts
from kijiji_mapper.render import render_map

from kijiji_mapper import (
    FAKE_USER_AGENT,
    DEFAULT_PAGES,
    DEFAULT_URL_TEMPLATE,
    TEMPLATE_NAME,
    JS_API_KEY,
    DEFAULT_MAP_CENTER,
)


def run():
    post_generator = yield_posts(
        DEFAULT_URL_TEMPLATE, DEFAULT_PAGES, FAKE_USER_AGENT)
    posts = [x for x in post_generator]
    print(render_map(posts, TEMPLATE_NAME, JS_API_KEY, DEFAULT_MAP_CENTER))
