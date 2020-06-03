import time
import os
import shutil
import uuid
import logging
import zipfile
import os.path
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import tempfile
from os import walk, path, rename, mkdir

import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def scrape_sites(event, download_dir):

    def is_empty(any_structure):
        if any_structure:
            # print('Structure is not empty.')
            return False
        else:
            # print('Structure is empty.')
            return True
    # TODO: pass in time id to function; for now hard code here

    strftime_format = ("%Y-%m-%d_%H.%M.%S")

    logger.info("-----Create Folders-----")

    tmp_folder = tempfile.TemporaryDirectory()
    tmp_folder = tmp_folder.name
    
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    if not os.path.exists(tmp_folder + '/user-data'):
        os.makedirs(tmp_folder + '/user-data')

    # download_dir = tmp_folder + '/download-data/'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    logger.info("----/Create Folders-----")

    logger.info("-----Setup and run Selenium-----")

    options = webdriver.ChromeOptions()

    driver_path = "../bin/chromedriver.exe"
    # options.binary_location = './bin/headless-chromium'

    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--single-process')
    #
    # options.add_argument('--disable-gpu')
    # options.add_argument('--window-size=1280x1696')
    # options.add_argument('--user-data-dir={}'.format(tmp_folder + '/user-data'))
    # options.add_argument('--hide-scrollbars')
    # options.add_argument('--enable-logging')
    # options.add_argument('--log-level=0')
    # options.add_argument('--data-path={}'.format(tmp_folder + '/data-path'))
    # # #options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--homedir={}'.format(tmp_folder))
    # options.add_argument('--disk-cache-dir={}'.format(tmp_folder + '/cache-dir'))

    # prefs = {"profile.default_content_settings.popups": 0,
    #          "download.prompt_for_download": False,
    #          "safebrowsing_for_trusted_sources_enabled": False,
    #          "safebrowsing.enabled": False,
    #          "download.default_directory": download_dir,
    #          "directory_upgrade": True}

    prefs = {"profile.default_content_settings.popups": 0,
                   "download.prompt_for_download": "false",
                   "safebrowsing_for_trusted_sources_enabled": "false",
                   "safebrowsing.enabled": "false",
                   "download.default_directory": download_dir,
                   "directory_upgrade": "true"}

    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(driver_path, chrome_options=options)

    logger.info("----/Setup and run Selenium-----")


    logger.info("----Change download folder-----")

    # function to take care of downloading file
    # def enable_download_headless(browser, download_dir):
    #     browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    #     params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    #     browser.execute("send_command", params)
    #
    # enable_download_headless(driver, download_dir)

    logger.info("---/Change download folder-----")


    logger.info("---- Start Scraping -----")

    #data = json.loads(open('/docs/commands.json').read())
    data = event
    logger.info(data)
    delay = 3
    short_delay = 1

    try:

        zip_list = []

        for k, v in data["selenium_commands"].items():

            status = {}
            zip_name = ""

            logger.info("------start loop--------------------------------")

            date_time = time.strftime("%Y-%m-%d_%H.%M.%S")
            tmp_path = tempfile.mkdtemp()
            tmp_path_slash = tmp_path + os.sep
            tmp_path_screenshots = os.path.join(tmp_path_slash + "screenshots" + os.sep)
            mkdir(tmp_path_screenshots)
            tmp_path_pagesource = os.path.join(tmp_path_slash + "pagesource" + os.sep)
            mkdir(tmp_path_pagesource)
            tmp_path_download = os.path.join(tmp_path_slash + "download" + os.sep)
            mkdir(tmp_path_download)

            step = v["step"]
            send_keys_to_elements = v["send_keys_to_elements"]
            perform_download = v["perform_download"]
            prepend_to_name = v["prepend_to_name"]
            final_click = v["final_click"]
            css_button = v["css_button"]
            urls = v["urls"]
            save_page_source = v["save_page_source"]

            # 0. Start building a log response object;
            logger.info("   ---step---   ")
            logger.info(k)
            logger.info(step)
            logger.info("   --/step---   ")

            # 1. Try and get url - if fails, log
            logger.info("   ---urls---   ")
            logger.info(urls)
            try:
                driver.get(urls)
                time.sleep(delay)
                html_str = driver.page_source

                if html_str == '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body></body></html>' or "This site can’t be reached" in html_str:
                    logger.warning("unable to connect to " + urls)
                    status["get_url"] = "failure"
                else:
                    status["get_url"] = "success"
            except:
                pass
                # break out of for loop
                # respond with failure
                logger.warning("unable to connect to " + urls)
                status["get_url"] = "failure"
                continue

            if status["get_url"] != "failure":
                logger.info("   --/urls---   ")

                # if succesful, send all send Keys. If fails, log (and get screenshot), but continue
                # loop through all send_keys
                logger.info("   ---send_keys---   ")
                try:
                    if send_keys_to_elements and isinstance(send_keys_to_elements, dict):

                        for sendK, sendV in send_keys_to_elements.items():
                            if sendV["value"] == "SEND_KEYS-ENTER":
                                elem.send_keys(Keys.RETURN)
                                time.sleep(delay)
                                driver.get_screenshot_as_file(
                                    tmp_path_screenshots +
                                    "step-" +
                                    str(step) +
                                    "hiitEnterInSendKey-" +
                                    time.strftime(strftime_format) +
                                    ".png"
                                )
                            else:
                                logger.debug("find element: " + sendV["value"])
                                elem = driver.find_element_by_xpath(sendV["value"])

                                logger.debug("clear element: " + sendV["value"])
                                elem.clear()

                                logger.debug("send key to element: " + sendV["value"])
                                elem.send_keys(sendV["send_key"])

                        if final_click == "SEND_KEYS-ENTER":
                            elem.send_keys(Keys.RETURN)
                            time.sleep(delay)
                            driver.get_screenshot_as_file(
                                tmp_path_screenshots +
                                "step-" +
                                str(step) +
                                "send_keys[PostSend]-" +
                                time.strftime(strftime_format) +
                                ".png"
                            )
                    status["send_keys"] = "success"
                except:
                    pass
                    # break out of for loop
                    # respond with failure
                    logger.warning("unable to send keys for " + urls)
                    status["send_keys"] = "unable to send keys for " + urls
                    continue


                logger.info("   --/send_keys---   ")

                # trigger the button clicks if any present, in the order they are present in the json
                logger.info("   ---css_buttons---   ")
                if css_button and isinstance(css_button, dict):

                    for cssK, cssV in css_button.items():
                        logger.info(cssV["buttonCSS"])
                        try:
                            button = driver.find_element_by_xpath(cssV["buttonCSS"])
                            status["css_button" + str(cssK)] = "success"
                        except:
                            logger.warning("Cannot find element: " + cssV["buttonCSS"])
                            status["css_button" + str(cssK)] = "Cannot find element: " + cssV["buttonCSS"]
                        else:
                            button.click()
                            time.sleep(short_delay)
                            driver.get_screenshot_as_file(
                                tmp_path_screenshots +
                                "css_button_" +
                                str(cssK) +
                                "-" +
                                time.strftime(strftime_format) +
                                ".png"
                            )

                else:
                    logger.info("css button empty")
                    status["css_button_empty"] = "success"

                logger.info("   --/css_buttons---   ")


                # trigger final button click
                logger.info("   ---final_click---   ")
                if final_click != "SEND_KEYS-ENTER":
                    if final_click != "":

                        try:
                            driver.get_screenshot_as_file(
                                tmp_path_screenshots +
                                "final_click_before" +
                                str(step) +
                                "-" +
                                time.strftime(strftime_format) +
                                ".png"
                            )
                            button = driver.find_element_by_xpath(final_click)
                        except:
                            logger.warning("ERROR - unable to click final click")
                            logger.warning("Cannot find elemennt: " + final_click)
                            status["final_click"] = "failure"
                        else:
                            button.click()
                            time.sleep(delay)
                            driver.get_screenshot_as_file(
                                tmp_path_screenshots +
                                "final_click_after" +
                                str(step) + "-" +
                                time.strftime(strftime_format) +
                                ".png"
                            )

                            # Move and rename the downloaded file(s)
                            if perform_download:
                                if os.path.isdir(download_dir):
                                    files = os.listdir(download_dir)

                                    if files:
                                        for f in files:
                                            shutil.move(download_dir + f, tmp_path_download)
                                            os.rename(tmp_path_download + f,
                                                      tmp_path_download + prepend_to_name + f)
                                    else:
                                        logger.warning("No files downloaded at step" + step)
                                else:
                                    logger.warning(download_dir + " - Directory does not exist; no files will be saved")

                        status["final_click"] = "success"

                    else:
                        logger.info("final click empty")
                        status["final_click"] = "success"
                else:
                    logger.info("no final click triggered as enter used in send_keys_to_elements process")

                logger.info("   --/final_click---   ")

                # get entire page source
                try:
                    if save_page_source:
                        with open(tmp_path_pagesource + step + "-" + date_time + ".html", "w", encoding="utf-8") as html_file:
                            f.write(html_str)

                except:
                    logger.info("Unable to save page source - check step name")
                #zip files

                def zipdir(path, ziph):
                    base_dir = os.path.basename(os.path.normpath(path))

                    # ziph is zipfile handle
                    for root, dirs, files in os.walk(path, topdown=True):
                        logger.info(root)
                        logger.info(dirs)
                        for file in files:
                            sub_folder = root.split(base_dir)
                            if sub_folder[1] == "":
                                ziph.write(os.path.join(root, file), arcname = file)
                            else:
                                ziph.write(os.path.join(root, file), arcname = os.path.join(sub_folder[1], file))

                zip_name = prepend_to_name + date_time + ".zip"
                zip_location = tmp_path + zip_name
                zipf = zipfile.ZipFile(zip_location, 'w', zipfile.ZIP_DEFLATED)
                zipdir(tmp_path, zipf)
                zipf.close()

            status_log = None
            zip_list.append({'step': step,
                             'status': status,
                             # 'status_log': status_log,
                             'local_location': tmp_path,
                             # 'bucket_name': bucket_name,
                             'zip_name': zip_name})

            logger.info("-----/next loop---------------------------------")
    except Exception as e:
        logger.error(e)
    finally:

        status_list = []
        for key in zip_list:
            status_list.append(list(key["status"].values()))

        zip_status_flattened = [val for sublist in status_list for val in sublist]
        set_flattened_zip = set(zip_status_flattened)

        if "failure" in set_flattened_zip:
            processing_status = "failure"
        elif set_flattened_zip and all(elem == "success" for elem in set_flattened_zip):
            processing_status = "success"
        else:
            processing_status = "partial-success"

        result_to_send = {'processing_results':zip_list,
                          'processing_status': processing_status}


    print(zip_list)

    # send message to sqs and return result
    json_return = json.dumps(result_to_send)
    print(json_return)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": json_return
        })
    }

    logging.info("----- Cleanup -----")

    driver.close()


