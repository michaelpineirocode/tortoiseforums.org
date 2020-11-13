import requests
import time
import os
from bs4 import BeautifulSoup
import threading

timestamp = str(time.time())
link = "https://www.tortoiseforum.org/"

req = requests.get(link)
soup = BeautifulSoup(req.text, "html.parser")

pageTitle = soup.find(class_="p-title-value").get_text() #gets the title of the page
root = "T:/" + pageTitle + " " + timestamp #assigns aroot path
os.mkdir(root) #makes root directory

block = soup.find_all(class_="block-container") #gets all the major blocks
currentpath = root
lastpath = None

def topic():
    global currentpath
    for b in block:
        if b.find(class_="block-header--left") != None:
            header = b.find(class_="block-header--left").get_text().replace("!", "")[1:-1]
            lastpath = currentpath
            currentpath = root + "/" + header
            os.mkdir(currentpath)
            subTopic(b, currentpath)
            currentpath = lastpath

def subTopic(block, path):
    global currentpath
    global lastpath
    content = block.find_all(class_="node-body")
    for c in content:
        title = c.find(class_="node-title").get_text().replace("\n", "").replace("?", "")
        meta = c.find(class_="node-meta").get_text().replace("\n\n\n", " ").replace("\n", "-").replace("'", "").replace("/", "")
        info = title + " " + meta
        lastpath = currentpath #stores what the last path will be before a change
        currentpath = currentpath + "/" + info
        os.mkdir(currentpath)
        currentpath = lastpath #sets the path back for the next iteration
        
topic()
