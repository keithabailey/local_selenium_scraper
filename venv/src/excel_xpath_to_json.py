from json import loads, dumps
from pandas import read_excel
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def build_selenium_commands(file_path = '../docs/xpath_example.xlsx'):

    df = read_excel(file_path, sheet_name='url')

    final_dict = {}

    for index, row in df.iterrows():

        sendKeysToElements = {}
        if isinstance(row['sendKeyElement'], str):

            sendKeyElements = row['sendKeyElement'].splitlines()
            sendKeyValues = row['sendKeyValues'].splitlines()

            #check that both lists are the same length
            if len(sendKeyElements) == len(sendKeyValues):

                for i in range(len(sendKeyElements)):
                    # "1": {"value": "#userid", "send_key": "raymond_lo@acl.com"}
                    tmp_dict1 = {
                        "value" : sendKeyElements[i],
                        "send_key" : sendKeyValues[i]
                    }
                    sendKeysToElements[i] = tmp_dict1

            else:
                logger.error("sendKeyElements and sendKeyValues do not have the same number of values")

        button_clicks = {}
        if isinstance(row['button_clicks'], str):

            buttons_tmp = row['button_clicks'].splitlines()

            # check that both lists are the same length

            for i in range(len(buttons_tmp)):
                # "1": {"value": "#userid", "send_key": "raymond_lo@acl.com"}
                tmp_dict2 = {
                    "buttonCSS": buttons_tmp[i]
                }
                button_clicks[i] = tmp_dict2


        tmp_dict3 = {"step": row['step'],
                    "send_keys_to_elements": sendKeysToElements,
                    "perform_download": row["perform_download"],
                    "prepend_to_name": row["prepend_to_name"],
                    "final_click": row["final_click"],
                    "css_button": button_clicks,
                    "urls": row["urls"],
                    "save_page_source": row["save_page_source"]
                    }

        final_dict[str(index)] = tmp_dict3

    print(final_dict)

    data = {"selenium_commands": final_dict}

    return(data)
