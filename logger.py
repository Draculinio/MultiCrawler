import logging
import datetime

class logger:
    def __init__(self):
        self.log_file='crawlerlog.log'
        logging.basicConfig(filename=self.log_file,level=logging.DEBUG)

    def log(self,text,level):
        text = str(datetime.datetime.now())+' :> '+text
        if level== 'info':
            logging.info(text)
        if level =='warning':
            logging.warning(text)
        if level=='error':
            logging.error(text)
        if level=='critical':
            logging.critical(text)