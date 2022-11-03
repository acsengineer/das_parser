import os
from dotenv import load_dotenv
import fake_useragent
import requests
from bs4 import BeautifulSoup
import doctest


load_dotenv()

if not os.path.isfile('./data/fuel.html'):
    session = requests.Session()

    url_ua = os.environ.get("URL_UA")
    user = fake_useragent.UserAgent().random

    header = {
        'user-agent': user
    }
    data = {
        'UserName': os.environ.get("USERNAME_UA"),
        'Password': os.environ.get("PASSWORD_UA")
    }

    response = session.post(url_ua, data=data, headers=header).text

    fuel_info = os.environ.get("URL_FUEL_INFO")
    fuel_info_res = session.get(fuel_info, headers=header).text

    with open("./data/fuel.html", "w") as file:
        file.write(fuel_info_res)

with open("./data/fuel.html") as file:
    fuel_info_res = file.read()

soup = BeautifulSoup(fuel_info_res, "lxml")

today_date = soup.find("input", id="cal")
print(today_date.get("value"))

all_fieldset = soup.find_all("legend")
for item in all_fieldset:
    if item.text == "Калорийность":
        fieldset_caloric = item.find_parent("fieldset")
        break

div_caloric = fieldset_caloric.find_all("div", class_="p")
for cal in div_caloric:
    cal_name = cal.find("div", class_="pn").text
    cal_value = cal.find("div", class_="cn d").text.replace('\xa0', '')  # \xa0 == &nbsp
    print(f"{cal_name}: {cal_value}")
    cal_value_int = int(cal_value)
