##### this script does the following: 
##### 1) it scrapes html data from a basketball website
##### 2) it saves the html to disk
#### The html has to be saved, because otherwise reason Canopy gets really slow after the scraping. 

#######################################################
##### Code for getting html from websites with javascript
#### This code is mostly borrowed from http://josechristian.com/2013/10/14/scraping-html-generated-by-javascript-python/
#### with slight modifications by me.

import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *

def save_html(url):

    
    class Render(QWebPage):
        def __init__(self, url):
    
            try:
                self.app = QApplication(sys.argv)
            except RuntimeError:  ### QApplication already exists
                self.app=QApplication.instance()
    
            QWebPage.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.mainFrame().load(QUrl(url))
            self.app.exec_()
    
        def _loadFinished(self, result):
            self.frame = self.mainFrame()
            self.app.quit()
    
    def getHtml(str_url):
        r_html = Render(str_url)
        html = r_html.frame.toHtml()
    
        return html
    
    html=getHtml(url)

    ##############
    ### saving
    ###########
    if base_url=='http://wvustats.com/mbasketball/':
        f = open('basketball.html','w')
    else:
        f = open(url[-5:]+'.html','w')
        
    
    f.write(html.encode('utf-8'))
    f.close()




#### base url (http://wvustats.com/mbasketball/) saved as basketball.html 
base_url='http://wvustats.com/mbasketball/'
save_html(base_url)

#####################################
##### getting all of the individual game links, and saving the html from each
###################################
from bs4 import BeautifulSoup
import re

html=open('basketball.html','r')
soup=BeautifulSoup(html.read(),'lxml')

games=soup.body.find_all('a',{'href':re.compile('http://wvustats.com/mbasketball/game/*')}) 
game_links=[x['href'] for x in games]

for links in game_links:
    save_html(links)
    
