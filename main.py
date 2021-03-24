import undetected_chromedriver as uc
from csv import DictWriter
from selenium import webdriver
import os

options = webdriver.ChromeOptions()

options.binary_location = os.environ.get('GOOGLE_CHROME_SHIM', None)
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path="chromedriver", options=options)


def get_url(k, l, c):
    return f"https://play.google.com/store/search?q={k}&c=apps&hl={l}&gl={c}"


def get_headless_window(url):
    driver.get(url=url)


# parametirise url +
# find app id # in a list +
# create a simple webform +
# connect webform with script +
# put output in a csv and download it after click on button +
# remove file after downloading +
# fix bugs +
# remove debug+
# switch parameter from language to country
# add input field for language


def get_web_elements(xpath):
    return driver.find_elements_by_xpath(xpath)


def find_app_id_index(app_id):
    app_id_xpath = "/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/c-wiz/c-wiz/c-wiz/div/div[2]/div"
    list_of_apps = get_web_elements(app_id_xpath)
    app_id_list = []
    for app in list_of_apps:
        app_id_list.append(app.find_element_by_tag_name("a").get_attribute("href"))
    try:
        i = app_id_list.index(f"https://play.google.com/store/apps/details?id={app_id}")
    except ValueError:
        i = "app is not in the first 50th list"
        return i
    else:
        return i + 1


def add_into_csv(input_data):
    fieldnames = ["KEYWORD", "INDEX"]
    with open("output.csv", 'a') as o:
        writer_object = DictWriter(o, fieldnames=fieldnames)
        writer_object.writerow(input_data)
        o.close()


def prepare_keyword(keyword):
    k1 = keyword.replace('\r\n', ",")
    new_keyword = k1.split(",")
    return new_keyword


def run_script(data):
    keywords = prepare_keyword(data['keyword'])
    for key in keywords:
        if len(key) > 1:
            new_key = key.lstrip()
            url = get_url(new_key.replace(" ", "%20"), data['locale'], data['country'])
            get_headless_window(url)
            add_into_csv({"KEYWORD": new_key, "INDEX": find_app_id_index(data['app_id'])})
