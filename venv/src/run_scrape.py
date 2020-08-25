import logging
import ast
import shutil
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from excel_xpath_to_json import build_selenium_commands
from local_scraper import scrape_sites

selenium_commands = build_selenium_commands(file_path = '../docs/marketdata_grab_xpath.xlsx.xlsx')
result = scrape_sites(selenium_commands, download_dir = "C:\\Users\\keith_bailey\\Downloads\\scrape-data\\")

# grab zip (only one for concur), unzip and rename file
body = ast.literal_eval(result["body"])
message = ast.literal_eval(body["message"])
processing_results = message["processing_results"]

# loop through all files in directory and copy over
src = processing_results[1]["local_location"] + "\\download\\"
src_files = os.listdir(src)
for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, "concur_zip.zip")
        
# delete concur_report.csv so we can create a new one without issue
location = "./report_output/"

if os.path.exists(location + "concur_report.csv"):
  os.remove(location + "concur_report.csv")
else:
  logger.info("concur_report.csv does not exist")

if processing_results[1]["status"]["get_url"] == "success" and processing_results[1]["status"]["get_url"] == "success" and processing_results[1]["status"]["get_url"] == "success":

    # unzip file & rename csv to concur_output.csv
    import zipfile

    with zipfile.ZipFile("./concur_zip.zip", 'r') as zip_ref:
        zip_ref.extractall(location)

    for file_name in os.listdir(location):
        if file_name.endswith('.csv'):
            os.rename(location + file_name, location + "concur_report.csv")
        else:
            os.remove(location + file_name)


