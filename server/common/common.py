import requests
from slugify import slugify
from datetime import datetime
from lxml.html import fromstring


# expects timestamp in seconds
def to_local_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%D")


def slugify_keys(d):
    return dict(
        (slugify(k.replace("regularMarket", ""), separator="_"), v)
        for k, v in d.items()
    )


def get_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath("//tbody/tr")[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join(
                [i.xpath(".//td[1]/text()")[0], i.xpath(".//td[2]/text()")[0]]
            )
            proxies.add(proxy)
    return proxies
