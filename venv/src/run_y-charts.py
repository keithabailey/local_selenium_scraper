import logging
import ast
import shutil
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from excel_xpath_to_json import build_selenium_commands
from local_scraper import scrape_sites
import time

selenium_commands = build_selenium_commands(file_path = '../docs/marketdata_grab_xpath.xlsx')
selenium_commands = build_selenium_commands(file_path = '../docs/qtryoygrowth_grab_xpath.xlsx')
# selenium_commands = build_selenium_commands(file_path = '../docs/sevicenow.xlsx')
result = scrape_sites(selenium_commands,
                      download_dir = "C:\\Users\\keith_bailey\\Downloads\\scrape-data\\",
                      headless = True)

# grab zip (only one for concur), unzip and rename file
body = ast.literal_eval(result["body"])
message = ast.literal_eval(body["message"])
processing_results = message["processing_results"]
location = "./report_output/"

date_time = time.strftime("%Y-%m-%d_%H.%M.%S")

for result in processing_results:
    # loop through all files in directory and copy over
    src = result["local_location"] + "\\download\\"

    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, location + file_name.replace(".csv","") + date_time + ".csv")


