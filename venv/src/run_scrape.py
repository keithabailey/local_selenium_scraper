import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from excel_xpath_to_json import build_selenium_commands
from local_scraper import scrape_sites

selenium_commands = build_selenium_commands(file_path = '/docs/concur_grab_xpath.xlsx')
scrape_sites(selenium_commands)