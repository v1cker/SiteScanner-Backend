from bs4 import BeautifulSoup
from register_site.models import WatchersIndex, RedirectionsIndex


def get_title(response):
    soup = BeautifulSoup(response.content)
    title = soup.title.string.strip() if soup.title else ''
    return title


def get_description(response):
    soup = BeautifulSoup(response.content)
    description = soup.find(attrs={"name": "description"}).attrs['content'] if soup.find(
        attrs={"name": "description"}) else ''
    return description


def get_h1(response):
    soup = BeautifulSoup(response.content)
    if soup.h1:
        h1 = soup.h1.string
    else:
        h1 = ''
    return h1


def get_redirection_code(response):
    if len(response.history) > 0:
        status_code = response.history[0].status_code
    else:
        status_code = response.status_code
    return status_code
