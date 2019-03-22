import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import mysql.connector
import logging
import dattetime

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

    get_html_code: Gets the html of an url
    get_all_links: gets all the links of a given url
    discard_internal_links: deletes internal links from list
    get_domain: Gets the domain of the url
    convert_domain_links: adds the domain to links from the same site.
    discard_non_type: Cleans the links list from non types.
    """
    def __init__(self,url):
        self.url=url
        self.domain=''
        self.html_code=''
        self.links_list = []
        self.title = ''
        
    """
    Gets the HTML code of a URL
    """
    def get_html_code(self,verbose=False):
        self.html_code=BeautifulSoup(requests.get(self.url).content,features="html.parser")
        self.title = self.html_code.title.string
        if verbose==True:
            log =logger()
            log.log('Code found! on site '+self.url,'info')
            log.log("Page Title: "+self.title,'info')
            

    """
    Gets all the links from the sourcecode of a site.
    """
    def get_all_links(self,verbose=False):
        log=logger()
        if verbose:
            log.log('Getting all the links for '+self.url,'info')
        self.links_list=[]
        links = self.html_code.findAll("a")
        for link in links:
            try:
                self.links_list.append(link.get('href'))
                if verbose==True:
                    log.log("Found link: "+self.links_list[-1],'info')
            except:
                log.log("Non Type found",'warning')

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
        
        
    """
    Discards elements that start with # (internal links or anchors)
    """
    def discard_internal_links(self,verbose=False):
        log = logger()
        new_link = []
        if verbose:
            log.log("Discarding internal links",'info')
        for link in self.links_list:
            try:
                if link[0]!='#':
                    new_link.append(link)
                else:
                    if verbose==True:
                        log.log("Link: "+self.links_list[i]+" is internal, it will be deleted",'info')
            except:
                log.log('Didnt find a value for zero char','info')
                
        self.links_list = new_link

    def discard_invalid_links(self,verbose=False):
        new_link = []
        log =logger()
        if verbose:
            log.log('Discarding internal links','info')
        for link in self.links_list:
            try:
                if 'http' in link:
                    new_link.append(link)
                else:
                    if verbose==True:
                        log.log("Link: "+link+" is not a valid link, it will be deleted",'info')
            except:
                log.log('Didnt find a value for zero char','warning')
        self.links_list = new_link
        
    """
    Gets the domain
    This is useful for links that goes inside the site.
    """
    def get_domain(self,verbose=False):
        log=logger()
        self.domain = urlparse(self.url)
        self.domain = self.domain.scheme + '://'+self.domain.netloc
        if verbose:
            log.log("domain: "+self.domain,'info')
        
    """
    Adds domain to links that start with /
    """
    def convert_domain_links(self,verbose=False):
        log=logger()
        for link in self.links_list:
            try:
                
                if link[0]=='/':
                    link=self.domain+link
                    if verbose==True:
                        log.log("Link converted to "+link,'info')
            except:
                log.log('Didnt find a value for zero char','warning')

    """
    Prints the actual list of links
    """
    def print_list_links(self):
        print("--------------------LIST OF LINKS FOUND--------------------------")
        for link in self.links_list:
            print(link)
        print("------------------END OF LIST OF LINKS FOUND---------------------")
                
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

    """Marks a site as used, so it won't go again there"""
    def mark_site_as_used(self,link):
        print("here the site will be marked")

    def add_title(self,link,title):
        try:
            self.execute_query("update sites set title = '"+title+"' where site_url='"+link+"'",False,True)
        except Exception as e:
            print(str(e))

    def get_site(self):
        return self.execute_query("select site_url from sites where used=0 order by site_id asc Limit 1")[0][0]

    def mark_site(self,link):
        try:
            self.execute_query("update sites set used = 1 where site_url='"+link+"'",False,True)
        except Exception as e:
            print(str(e))

class logger:
    def __init__(self):
        self.log_file='crawlerlog.log'
        logging.basicConfig(filename=self.log_file,level=logging.DEBUG)

    def log(self,level,text):
        text = str(datetime.datetime.now())+' :> '+text
        if level== 'info':
            logger.info(text)
        if level =='warning':
            logger.warning(text)
        if level=='error':
            logger.error(text)
        if level=='critical':
            logger.critical(text)
    
        
class crawler:
    def __init__(self,url,verbose):
        self.url = url
        self.verbose=False

    def crawl(self):
        while True:
            dm = database_manager()
            lm = link_manager(self.url)
        
            lm.get_domain(self.verbose)
            lm.get_html_code(False)
            lm.get_all_links(True)
            lm.discard_non_type()
            lm.discard_internal_links(self.verbose)
            lm.convert_domain_links(True)
            lm.discard_invalid_links(True)
            lm.print_list_links()
        
        
            dm.connector('localhost','generic_user','generic_password','multicrawler')
            dm.insert_sites(lm.links_list)
            dm.add_title(lm.url,lm.title)
            dm.mark_site(lm.url)
            self.url=dm.get_site()

crawl = crawler('https://www.crummy.com/software/BeautifulSoup/',False)
crawl.crawl()
