from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import os, sys, logging, time

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from src.webdriver.proxy import get_proxy

class Driver:

    driver = None
    logger = logging.getLogger("webdriver")
    active_headless = True
    block_cookie = False
    n_swith_port = 10

    @classmethod
    def setup(cls, url):
        """ Loading the browser """
        if cls.driver != None:
            return
        try:
            cls.logger.debug("################################### SETUP ###################################")
            chrome_options = webdriver.ChromeOptions()
            
            # proxy = get_proxy()
            # cls.setting_proxy = proxy
            # if proxy:
            #     cls.logger.debug("proxy found")
            #     cls.logger.debug(proxy)
            #     chrome_options.add_argument(f"--proxy-server={proxy}")
            # else:
            #     cls.logger.debug("no proxy found")
            
            chrome_options.add_argument("--proxy-bypass-list=<-loopback>")
            chrome_options.add_argument("--disable-features=NetworkService")  # Chrome < 114
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")

            if cls.block_cookie:
                chrome_options.browser_version = '125'
                chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})


            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox") 
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-breakpad")  # désactive crashpad
            chrome_options.add_argument("--disable-crash-reporter")
            chrome_options.add_experimental_option("detach", False)

            chrome_options.add_argument("--disable-in-process-stack-traces")
            chrome_options.add_argument("--noerrdialogs")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-logging")

            
            # Use local Chrome WebDriver with fallback options for different environments
            cls.logger.debug("Setting up Chrome WebDriver")
            
            # Set Chrome binary path if available (for Nix/Replit environments)
            chrome_bin = os.getenv("CHROME_BIN")
            if chrome_bin:
                chrome_options.binary_location = chrome_bin
                cls.logger.debug(f"Using Chrome binary: {chrome_bin}")
            
            try:
                # Try using webdriver-manager first (works on most systems)
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                
                service = Service(ChromeDriverManager().install())
                cls.driver = webdriver.Chrome(service=service, options=chrome_options)
                cls.logger.debug("Chrome WebDriver setup successful with webdriver-manager")
                
            except Exception as e:
                cls.logger.warning(f"webdriver-manager failed: {e}")
                
                try:
                    # Fallback: try using system Chrome
                    cls.driver = webdriver.Chrome(options=chrome_options)
                    cls.logger.debug("Chrome WebDriver setup successful with system Chrome")
                    
                except Exception as e2:
                    cls.logger.error(f"System Chrome failed: {e2}")
                    
                    # Try with chromedriver path from environment
                    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
                    if chromedriver_path:
                        try:
                            service = Service(chromedriver_path)
                            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
                            cls.logger.debug("Chrome WebDriver setup successful with environment chromedriver")
                        except Exception as e3:
                            cls.logger.error(f"Environment chromedriver failed: {e3}")
                    
                    # Final fallback: try with chromedriver in PATH
                    if not cls.driver:
                        try:
                            service = Service("chromedriver")
                            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
                            cls.logger.debug("Chrome WebDriver setup successful with PATH chromedriver")
                        except Exception as e4:
                            cls.logger.error(f"PATH chromedriver failed: {e4}")
                    
                    if not cls.driver:
                        raise Exception("Could not initialize Chrome WebDriver. Please ensure Chrome and ChromeDriver are installed.")
            

            logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
            logging.getLogger('selenium.webdriver.common.driver_finder').setLevel(logging.WARNING)
            logging.getLogger('selenium.webdriver.common.service').setLevel(logging.WARNING)
            logging.getLogger('webdriver_manager').setLevel(logging.WARNING)
            logging.getLogger('urllib3').setLevel(logging.WARNING)            

        except Exception as e:
            cls.logger.error("Error while setting up the driver")
            cls.logger.error(e)

    @classmethod
    def page_url(cls, url):

        # signal.signal(signal.SIGTERM, cls.terminate_process)
        cls.logger.debug("############################### START PAGE " + url + " ###################################")
        
        code_html = ""
        retry = True
        n_retry = 0
        cls.logger.debug("############################### START WHILE " + str(n_retry) + " ###################################")
        while retry and 5 > n_retry:
            cls.logger.debug("############################## RETRY " + str(n_retry) + " ###################################")
            code_html = cls.__page(url)
            blocked_bool = cls.check_if_page_is_blocked(code_html)
            if not blocked_bool:
                retry = False
            else:
                n_retry += 1
                cls.logger.warning("driver quit in page function " + url)
                cls._safe_quit()
        cls.logger.debug("############################### END WHILE " + str(n_retry) + " ###################################")
        if blocked_bool:
            raise ValueError("HTML PAGE IS EMPTY " + url)
        
        cls.logger.debug("############################### END PAGE " + url + " ###################################")

        codes_html = [code_html]

        #click button to go to next page
        try:
            cls.logger.debug("Trying to find next page button")
            wait = WebDriverWait(cls.driver, 10)  # Timeout de 10 secondes
            next_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "next")))
    
            while next_button:
                cls.logger.debug("Next page button found, clicking it")
                next_button.click()
                cls.logger.debug("Waiting for the next page to load")
                time.sleep(5)  # Adjust wait time as needed
                next_page_html = cls.driver.page_source
                codes_html.append(next_page_html)
                next_button = cls.driver.find_element(By.CLASS_NAME, "next")
        except Exception as e:
            cls.logger.warning(f"Could not find or click next page button: {e}")
        
        
        return codes_html
    
    @classmethod
    def page(cls, url):

        # signal.signal(signal.SIGTERM, cls.terminate_process)
        cls.logger.debug("############################### START PAGE " + url + " ###################################")
        
        code_html = ""
        retry = True
        n_retry = 0
        cls.logger.debug("############################### START WHILE " + str(n_retry) + " ###################################")
        while retry and 5 > n_retry:
            cls.logger.debug("############################## RETRY " + str(n_retry) + " ###################################")
            code_html = cls.__page(url)
            blocked_bool = cls.check_if_page_is_blocked(code_html)
            if not blocked_bool:
                retry = False
            else:
                n_retry += 1
                cls.logger.warning("driver quit in page function " + url)
                cls._safe_quit()
        cls.logger.debug("############################### END WHILE " + str(n_retry) + " ###################################")
        if blocked_bool:
            raise ValueError("HTML PAGE IS EMPTY " + url)
        
        cls.logger.debug("############################### END PAGE " + url + " ###################################")

        return code_html


    @classmethod
    def check_if_page_is_blocked(cls, html: str) -> bool:
        """Detect if the HTML page indicates blocking or an error."""

        # Liste des motifs de blocage connus
        known_blocking_signatures = {
            "may take a few seconds": "Page may be temporarily unavailable",
            "you have been blocked": "Access has been explicitly blocked",
            "This site can’t be reached": "Generic network error",
            "ERR_TOO_MANY_RETRIES": "Too many retries, possibly due to rate limiting"
        }

        # Vérifie si l'un des motifs de blocage est présent dans le HTML
        for pattern, explanation in known_blocking_signatures.items():
            index = html.find(pattern)
            if index != -1:
                cls.logger.warning("Detected blocking pattern in HTML")
                cls.logger.warning(f"Pattern: '{pattern}' — {explanation}")

                # Extrait un extrait du HTML autour du motif détecté
                context_radius = 200
                start = max(0, index - context_radius)
                end = min(len(html), index + len(pattern) + context_radius)
                snippet = html[start:end].replace('', ' ').replace('\r', ' ')
                cls.logger.warning(f"Context snippet: [...] {snippet} [...]")

                return True

        # Vérifie si la page est anormalement courte
        minimum_acceptable_size = 2000
        actual_size = len(html)

        if actual_size < minimum_acceptable_size:
            cls.logger.warning("HTML page appears too small — possible block or error")
            cls.logger.warning(f"Page size: {actual_size} bytes (expected at least {minimum_acceptable_size})")

            # Log d’un extrait complet si possible (limité à 500 caractères max)
            preview = html[:500].replace('', ' ').replace('\r', ' ')
            cls.logger.warning(f"HTML preview: {preview} [...]")
            return True

        # Aucun blocage détecté
        return False


    @classmethod
    def __page(cls, url):
        """ Loading the page and waiting until classname is present"""
        
        if cls.driver == None or cls.isClosed():
            cls.driver = None
            cls.setup(url)
        try:
            cls.logger.debug("Loading page " + url)
            cls.driver.get(url)
        except Exception as e:
            cls.logger.error(e)
            cls.logger.warning("driver quit in __page")
            cls._safe_quit()

        if cls.driver == None or cls.isClosed():
            return ""
        else:            
            return cls.driver.page_source


    @classmethod
    def isClosed(cls):
        """ check if browser is still open"""
        try:
            cls.driver.current_url
            return False
        except:
            return True

    @classmethod
    def terminate_process(cls, signum=None, frame=None):
        cls.logger.info("TERMINATE PROCESSUS SELENIUM")
        if cls.driver:
            cls.driver.quit()
        sys.exit(0)

    @classmethod
    def _safe_quit(cls):
        if cls.driver:
            try:
                cls.logger.warning("driver quit in _safe_quit")
                cls.driver.quit()
            except Exception as e:
                cls.logger.warning("Erreur lors de la fermeture du driver: " + str(e))

