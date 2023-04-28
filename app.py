# import requests
# from bs4 import BeautifulSoup
# import xml.etree.ElementTree as ET
# from fastapi import FastAPI
# import json


# # URL of the Interpol website to scrape
# url = 'https://www.interpol.int/How-we-work/Notices/View-UN-Notices-Individuals#2021-69573'

# # Make a request to the website and get the HTML content
# response = requests.get(url)
# html_content = response.content

# # Parse the HTML content using BeautifulSoup
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find all the notices on the page
# notices = soup.find_all('div', {'class': 'notice'})

# # Create the root element of the XML document
# root = ET.Element('notices')

# # Loop over each notice and extract the relevant data
# for notice in notices:
#     name = notice.find('div', {'class': 'notice-name'}).text
#     forename = notice.find('div', {'class': 'notice-forename'}).text
#     patronymic = notice.find('div', {'class': 'notice-patronymic'}).text
#     dob = notice.find('div', {'class': 'notice-dob'}).text
#     pob = notice.find('div', {'class': 'notice-pob'}).text
#     comments = notice.find('div', {'class': 'notice-comments'}).text
    
#     # Create the notice element and append the data as subelements
#     notice_element = ET.SubElement(root, 'notice')
#     name_element = ET.SubElement(notice_element, 'name')
#     name_element.text = name
#     forename_element = ET.SubElement(notice_element, 'forename')
#     forename_element.text = forename
#     patronymic_element = ET.SubElement(notice_element, 'patronymic')
#     patronymic_element.text = patronymic
#     dob_element = ET.SubElement(notice_element, 'date_of_birth')
#     dob_element.text = dob
#     pob_element = ET.SubElement(notice_element, 'place_of_birth')
#     pob_element.text = pob
#     comments_element = ET.SubElement(notice_element, 'comments1')
#     comments_element.text = comments

# # Write the XML document to a file
# tree = ET.ElementTree(root)
# tree.write('notices.xml')




# app = FastAPI()

# @app.get("/notices")
# async def read_notices():
#     # Parse the XML file
#     tree = ET.parse('notices.xml')
#     root = tree.getroot()

#     # Loop over each notice and extract the data
#     notices = []
#     for notice in root.findall('notice'):
#         name = notice.find('name').text
#         forename = notice.find('forename').text
#         patronymic = notice.find('patronymic').text
#         dob = notice.find('date_of_birth').text
#         pob = notice.find('place_of_birth').text
#         comments = notice.find('comments1').text

#         # Create a dictionary with the notice data and append it to the list
#         notice_dict = {'name': name, 'forename': forename,'patronymic': patronymic, 'date_of_birth': dob, 'place_of_birth': pob, 'comments1': comments}
#         notices.append(notice_dict)

#     # Convert the list of notices to a JSON string and return it
#     return json.dumps(notices)


import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# путь к драйверу chrome
chromedriver = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

url = 'https://www.interpol.int/How-we-work/Notices/View-UN-Notices-Individuals'
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

table_data = []
if response.status_code == 200:
    tree = ET.ElementTree(ET.Element('data'))
    root = tree.getroot()

    for td in response.text.split('<td')[1:]:
        td_value = td.split('>')[1].split('<')[0].strip()
        td_value += '\n'
        value = ET.Element('value')
        value.text = td_value
        root.append(value)
    
    tree = ET.ElementTree(root)
    tree.write('data.xml')
