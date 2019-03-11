import requests
from bs4 import BeautifulSoup

def get_html_code(site):
    return BeautifulSoup(requests.get(site).content,features="html.parser")

def get_all_links(code):
    return code.findAll("a")

code=get_html_code("https://es.wikipedia.org/wiki/J._R._R._Tolkien")
#print (code)
links = get_all_links(code)
print(links)
for link in links:
    print(link.get('href'))
