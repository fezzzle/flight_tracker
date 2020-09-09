import requests
from bs4 import BeautifulSoup
from flask import url_for

BASE_URL = f"https://www.jetphotos.com/photo/keyword/"

def plane_img(query):
    try:
        page = requests.get(BASE_URL + query)
        bs4 = BeautifulSoup(page.content, 'html.parser')
        search_link = bs4.find("a", "result__photoLink")
        result = f"https:{search_link.find('img')['src']}"
        return result
    except Exception as e:
        print(e)

    return url_for('static', filename='default.jpg')