import requests
from bs4 import BeautifulSoup
import re

def getLinks(filename):
    search_url = 'http://www.google.co.in/searchbyimage/upload'
    multipart = {'encoded_image': (filename, open(filename, 'rb')), 'image_content': ''}
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',})
    response = requests.post(search_url, files = multipart, allow_redirects = False, headers = headers)
    imgsearch_url = response.headers['Location']
    print(imgsearch_url)
    page = requests.get(imgsearch_url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a", href = True)
    return links
       
def getTags(filename):
    link_obj = getLinks(filename)
    all_links = [str(i.get("href")) for i in link_obj]
    clean_links = filterLinks(all_links)
    return all_links, clean_links

def filterLinks(a):
    return a



filename = r'Database/Images/sampleimg.png'
x,y = getTags(filename)