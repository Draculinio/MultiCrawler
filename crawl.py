import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import mysql.connector


class link_manager:

    def __init__(self,url):
        self.url=url
        self.domain=''
        self.html_code=''
        self.links_list = []
        
    """
    Gets the HTML code of a URL
    """
    def get_html_code(self,verbose=False):
        self.html_code=BeautifulSoup(requests.get(self.url).content,features="html.parser")
        if verbose==True:
            print(self.html_code)
        

    """
    Gets all the links from the sourcecode of a site.
    """
    def get_all_links(self):
        self.links_list=[]
        links = self.html_code.findAll("a")
        for link in links:
            self.links_list.append(link.get('href'))
        
    """
    Discards elements that start with # (internal links or anchors)
    """
    def discard_internal_links(self):
        for i in range(0,len(self.links_list)-1):
            link = self.links_list[i]
            try:
                if link[0]=='#':
                    del self.links_list[i]
            except:
                print('Didnt find a value for zero char')
                #TODO: Why are those appearing?????
        
    """
    Gets the domain
    This is useful for links that goes inside the site.
    """
    def get_domain(self):
        self.domain = urlparse(self.url)
        self.domain = self.domain.scheme + '://'+self.domain.netloc
        
    """
    Adds domain to links that start with /
    """
    def convert_domain_links(self):
        for i in range(0,len(self.links_list)-1):
            link = self.links_list[i]
            try:
                if link[0]=='/':
                    self.links_list[i]=self.domain+link
            except:
                print('Didnt find a value for zero char')
                #TODO: Why are those appearing?????
        
        

class database_manager:

    def __init__(self):
        self.db_connection = ''
    
    """
    Connects to the database
    """
    def connector(self,dbhost,dbuser,dbpassword,dbname,dbcharset='utf8'):
        self.db_connection=mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            password=dbpassword,
            database = dbname,
            charset = dbcharset)
        #print (self.db_connection)

    """
    Executes an SQL query
    """
    def execute_query(self,order,results=True,insertion=False):
        cursor = self.db_connection.cursor(buffered=True)
        cursor.execute(order)
        if insertion==True:
            self.db_connection.commit()
        if results==True:
            return cursor.fetchall()

    """
    Inserts sites into table if needed.
    """
    def insert_sites(self,links):
        for i in range(0,len(links)-1):
            site_existence_verification = self.execute_query("select count(*) from sites where site_url='"+links[i]+"'")
            if site_existence_verification[0][0]==0:
                self.execute_query("insert into sites (site_url,used) values ('"+links[i]+"',false)",False,True)
    


lm = link_manager('https://github.com/Draculinio')
lm.get_domain()
lm.get_html_code()
lm.get_all_links()
lm.discard_internal_links()
lm.convert_domain_links()

dm = database_manager()
dm.connector('localhost','generic_user','generic_password','multicrawler')
dm.insert_sites(lm.links_list)
