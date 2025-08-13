import os, sys, logging, re
from bs4 import BeautifulSoup

def html_url_parser(html_content):

    logger = logging.getLogger("HtmlParserUrl")
    try:
        soup = BeautifulSoup(str(html_content), 'html.parser')
        list_a = soup.find_all("a", class_="name")
        urls = list()
        for a in list_a:
            url = a.get('href')
            if is_valid_url(url):
                urls.append({"url": url})

    except Exception as e:
        logger.warning(str(e))
        urls = []
    return urls

def is_valid_url(url):
    """ regex check to valid if url is a real url """
    # Expression régulière pour vérifier les URL
    try:
        regex = re.compile(
            r'^(https?://)?'  # supporte http et https
            r'([a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+)'  # domaine
            r'(:\d+)?'  # port (optionnel)
            r'(/.*)?$'  # chemin (optionnel)
        )
        return re.match(regex, url) is not None
    except Exception as e:
        return False
