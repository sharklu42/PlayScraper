import undetected_chromedriver as uc
from csv import DictWriter

options = uc.ChromeOptions()

options.add_argument("--headless")

driver = uc.Chrome(options=options)


def get_url(k, c):
    return f"https://play.google.com/store/search?q={k}&c=apps&hl={c}&gl=US"


def get_headless_window(url):
    driver.get(url=url)


# parametirise url +
# find app id # in a list +
# create a simple webform +
# connect webform with script +
# put output in a csv and download it after click on button +
# remove file after downloading +
# fix bugs +
# remove debug


def get_web_elements(xpath):
    return driver.find_elements_by_xpath(xpath)


def find_app_id_index(app_id):
    app_id_xpath = "/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/c-wiz/c-wiz/c-wiz/div/div[2]/div"
    list_of_apps = get_web_elements(app_id_xpath)
    app_id_list = []
    for app in list_of_apps:
        app_id_list.append(app.find_element_by_tag_name("a").get_attribute("href"))
    i = app_id_list.index(f"https://play.google.com/store/apps/details?id={app_id}")
    return i + 1


def add_into_csv(input_data):
    fieldnames = ["KEYWORD", "INDEX"]
    with open("output.csv", 'a') as o:
        writer_object = DictWriter(o, fieldnames=fieldnames)
        writer_object.writerow(input_data)
        o.close()


def run_script(data):
    for key in data['keyword'].split(', '):
        url = get_url(key.replace(" ", "%20"), data['country'])
        get_headless_window(url)
        add_into_csv({"KEYWORD": key, "INDEX": find_app_id_index(data['app_id'])})
