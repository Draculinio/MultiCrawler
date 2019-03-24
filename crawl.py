import mysql.connector
from logger import *
from link_manager import *

                
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
        print("AAAAAAAAAA")
        site =  self.execute_query("select site_url from sites where used=0 order by site_id asc Limit 1")[0][0]
        print(site)
        return site

    def mark_site(self,link):
        try:
            print("Link to mark: "+link)
            self.execute_query("update sites set used = 1 where site_url='"+link+"'",False,True)
        except Exception as e:
            print(str(e))


    
        
class crawler:
    def __init__(self,url,verbose):
        self.url = url
        self.verbose=False

    def crawl(self):
        dm = database_manager()
        lm = link_manager(self.url)
        while True:
            print("Getting domain...")
            lm.get_domain(self.verbose)
            print("Domain retrieved... "+lm.domain)
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
            lm.url = self.url

crawl = crawler('https://www.crummy.com/software/BeautifulSoup/',False)
crawl.crawl()
