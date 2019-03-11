import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

"""
Gets the HTML code of a URL
"""
def get_html_code(site, verbose=False):
    html_code=BeautifulSoup(requests.get(site).content,features="html.parser")
    if verbose==True:
        print(html_code)
    return html_code

"""
Gets all the links from the sourcecode of a site.
"""
def get_all_links(code):
    links_list=[]
    links = code.findAll("a")
    for link in links:
        links_list.append(link.get('href'))
    return links_list

"""
Discards elements that start with # (internal links or anchors)
"""
def discard_internal_links(links):
    num=0
    for i in range(0,len(links)-1):
        #print(links[i])
        link = links[i]
        try:
            if link[0]=='#':
                del links[i]
        except:
            print('Didnt find a value for zero char')
        
    return links

"""
Gets the domain
This is useful for links that goes inside the site.
"""
def get_domain(site):
    domain = urlparse(site)
    site = domain.scheme + '://'+domain.netloc
    return site


    
print(get_domain("https://github.com/Draculinio/MultiCrawler"))
code=get_html_code("https://github.com/Draculinio/MultiCrawler")

links = get_all_links(code)
links = discard_internal_links(links)
print(links)
