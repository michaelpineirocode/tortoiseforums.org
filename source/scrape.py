import requests
from datetime import datetime
import os
from bs4 import BeautifulSoup
import threading

timestamp = datetime.now().strftime("%b-%d-%y ~ %H-%M-%S")
link = "https://www.tortoiseforum.org/"

req = requests.get(link)
soup = BeautifulSoup(req.text, "html.parser")

pageTitle = soup.find(class_="p-title-value").get_text() #gets the title of the page
root = "T:/" + pageTitle + " " + timestamp #assigns a root path
os.mkdir(root) #makes root directory

block = soup.find_all(class_="block-container") #gets all the major blocks
currentpath = root
lastpath = None

def topic(): #picks each topic
    global currentpath
    count = 0
    for b in block:
        if b.find(class_="block-header--left") != None:
            count += 1
            header = str(count) + " " + b.find(class_="block-header--left").get_text().replace("!", "")[1:-1]
            lastpath = currentpath
            currentpath = root + "/" + header
            os.mkdir(currentpath) #creates path
            subTopic(b, currentpath) #for each topic, goes to subtopic
            currentpath = lastpath

def subTopic(block, path): #picks a subtopic
    global currentpath
    global lastpath
    content = block.find_all(class_="node-body")
    count = 0
    for c in content:
        count += 1
        title = c.find(class_="node-title").get_text().replace("\n", "").replace("?", "")
        meta = c.find(class_="node-meta").get_text().replace("\n\n\n", " ").replace("\n", "-").replace("'", "").replace("/", "")
        info = str(count) + " " + title# + " " + meta
        sublink = c.find("a")["href"]
        lastpath = currentpath #stores what the last path will be before a change
        currentpath = currentpath + "/" + info #stores the new current path
        os.mkdir(currentpath) #makes the path
        selectForum(sublink) #calls a function which will select the forums to copy
        currentpath = lastpath #sets the path back for the next iteration
        
def selectForum(topiclink): #selects the forums
    page_number = 1
    req = requests.get(link + topiclink) #gets the content from the forum page
    soup = BeautifulSoup(req.text, "html.parser")
    block = soup.find(class_="p-body").find(class_="p-body-inner").find_all(class_="block")
    if len(block) == 2: 
        block.pop(0)
    
    nextButton = block[0].find("a")["href"]
    print(topiclink, nextButton)    

def copyForum(): #copies the forums
    pass

topic()
