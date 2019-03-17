import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import mysql.connector


class link_manager:
    """
    A class to extract information from pages and get links for the crawler

    Atributes
    ---------

    url: The url to inspect
    domain: the domain of the url
    html_code: the html of the url
    links_list: A list of links

    Methods
    -------

    get_html_code: Gets the html of an url}
    get_all_links: gets all the links of a given url
    discard_internal_links: deletes internal links from list
    get_domain: Gets the domain of the url
    convert_domain_links: adds the domain to links from the same site.
    """
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
            print("Code found: ")
            print(self.html_code)
        

    """
    Gets all the links from the sourcecode of a site.
    """
    def get_all_links(self,verbose=False):
        if verbose:
            print("Getting all links")
        self.links_list=[]
        links = self.html_code.findAll("a")
        for link in links:
            try:
                self.links_list.append(link.get('href'))
                if verbose==True:
                    print("Found link: "+self.links_list[-1])
            except:
                print("Non Type found")

    """
    Used to discard non types
    """
    def discard_non_type(self):
        new_link = []
        counter=0
        for link in self.links_list:
            if link is not None:
                new_link.append(link)
                counter=counter +1
        self.links_list = new_link
        print(counter)
        
    """
    Discards elements that start with # (internal links or anchors)
    """
    def discard_internal_links(self,verbose=False):
        if verbose:
            print("Discarding internal links")
        for link in self.links_list:
            #link = self.links_list[i]
            try:
                if link[0]=='#':
                    if verbose==True:
                        print("Link: "+self.links_list[i]+" is internal, it will be deleted")
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
    def convert_domain_links(self,verbose=False):
        for i in range(0,len(self.links_list)-1):
            link = self.links_list[i]
            try:
                if link[0]=='/':
                    self.links_list[i]=self.domain+link
                    if verbose==True:
                        print("Link converted to "+self.links_list[i])
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
        for link in links:
            site_existence_verification = self.execute_query("select count(*) from sites where site_url='"+link+"'")
            if site_existence_verification[0][0]==0:
                self.execute_query("insert into sites (site_url,used) values ('"+link+"',false)",False,True)

    def mark_site_as_used(self,link):
        print("here the site will be marked")

class crawler:
    def __init__(self,url,verbose):
        self.url = url
        self.verbose=verbose

    def crawl(self):
        lm = link_manager(self.url)
        lm.get_domain()
        lm.get_html_code(False)
        lm.get_all_links(self.verbose)
        lm.discard_non_type()
        lm.discard_internal_links(self.verbose)
        lm.convert_domain_links(self.verbose)

        dm = database_manager()
        dm.connector('localhost','generic_user','generic_password','multicrawler')
        dm.insert_sites(lm.links_list)

crawl = crawler('https://clarin.com/',False)
crawl.crawl()
