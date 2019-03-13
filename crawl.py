import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import mysql.connector

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
    for i in range(0,len(links)-1):
        #print(links[i])
        link = links[i]
        try:
            if link[0]=='#':
                del links[i]
        except:
            print('Didnt find a value for zero char')
            #TODO: Why are those appearing?????
        
    return links

"""
Gets the domain
This is useful for links that goes inside the site.
"""
def get_domain(site):
    domain = urlparse(site)
    site = domain.scheme + '://'+domain.netloc
    return site

"""
TODO: Describir el método
"""
def convert_domain_links(links,domain):
    for i in range(0,len(links)-1):
        link = links[i]
        try:
            if link[0]=='/':
                links[i]=domain+link
        except:
            print('Didnt find a value for zero char')
            #TODO: Why are those appearing?????
        
    return links


##DATABASE FUNCTIONS##
def connector():
    db_connection=mysql.connector.connect(
        host='localhost',
        user='generic_user',
        password='generic_password',
        database = 'multicrawler')
    return db_connection

"""
Executes an SQL query
"""
def execute_query(db_connection,order,results=True,insertion=False):
    cursor = db_connection.cursor(buffered=True)
    cursor.execute(order)
    if insertion==True:
        db_connection.commit()
    if results==True:
        return cursor.fetchall()

"""
Inserts sites into table if needed.
"""
def insert_sites(links,db_connection):
    for i in range(0,len(links)-1):
        site_existence_verification = execute_query(db_connection,"select count(*) from sites where site_url='"+links[i]+"'")
        if site_existence_verification[0][0]==0:
            execute_query(db_connection,"insert into sites (site_url,used) values ('"+links[i]+"',false)",False,True)
    

starting_domain = "https://github.com/Draculinio/MultiCrawler"
domain=get_domain(starting_domain)
code=get_html_code(starting_domain)

links = get_all_links(code)
links = discard_internal_links(links)
links = convert_domain_links(links,domain)
print(links)
db_connection = connector()
insert_sites(links,db_connection)
