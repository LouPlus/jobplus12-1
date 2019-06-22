from datetime import datetime


def add_link_suffix(url):
    return '{}?_={}'.format(url, datetime.utcnow().timestamp())
