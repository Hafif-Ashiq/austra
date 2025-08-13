import cloudscraper
import requests
import logging
from dotenv import load_dotenv  # Utilisé si vous utilisez un fichier .env
from src.webdriver.proxy import get_proxy

# Charger les variables d'environnement depuis un fichier .env (optionnel)
load_dotenv()

class Driver:

    logger = logging.getLogger("webdriver")

    def __init__(self):
        self.setup()

    def setup(self):
        """ Méthode de configuration initiale """
        logging.getLogger('urllib3').setLevel(logging.WARNING)

    def configure_proxy(self, url=None):
        """ Configure les paramètres du proxy pour la session """

        proxy_url = get_proxy() if url else None
        
        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }

        self.proxies = proxies

    def page(self, url):
        """ Charger la page en utilisant le proxy avec 3 tentatives """
        max_retries = 5
        for attempt in range(1, max_retries + 1):
            # self.configure_proxy(url)
            scraper = cloudscraper.create_scraper()
            try:
                self.logger.debug(f"Tentative {attempt} - URL: {url} ")
                # self.logger.debug(f"Tentative {attempt} - URL: {url} via proxies: {self.proxies}")
                response = scraper.get(
                    url,
                    # proxies=self.proxies,
                    timeout=60
                )
                response.raise_for_status()
                return response.text
            except (requests.exceptions.RequestException) as e:
                self.logger.warning(f"Tentative {attempt} échouée : {e}")
                if attempt == max_retries:
                    self.logger.error(f"Échec après {max_retries} tentatives.")
                    return None
            finally:
                scraper.close()  # 🧹 Nettoyage mémoire


    def isClosed(self):
        """ Cette fonction n'est pas nécessaire car nous n'ouvrons pas de navigateur """
        return False
