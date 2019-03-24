import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
import datetime

from logger import *

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
        self.log =logger()
        
    """
    Gets the HTML code of a URL
    """
    def get_html_code(self,verbose=False):
        try:
            self.html_code=BeautifulSoup(requests.get(self.url).content,features="html.parser")
            self.title = self.html_code.title.string
            if verbose==True:
                self.log.log('Code found! on site '+self.url,'info')
                self.log.log("Page Title: "+self.title,'info')
        except Exception as e:
            self.log.log('Error found: '+str(e),'error')    

    """
    Gets all the links from the sourcecode of a site.
    """
    def get_all_links(self,verbose=False):
        if verbose:
            self.log.log('Getting all the links for '+self.url,'info')
        self.links_list=[]
        links = self.html_code.findAll("a")
        for link in links:
            try:
                self.links_list.append(link.get('href'))
                if verbose==True:
                    self.log.log("Found link: "+self.links_list[-1],'info')
            except:
                self.log.log("Non Type found",'warning')

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