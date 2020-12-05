import requests
import uuid
from bs4 import BeautifulSoup
import os

class Website:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.content = BeautifulSoup(requests.get(self.url).text, "html.parser")

class Directory:
    def __init__(self, root, name, code=None):
        self.root = root
        self.subs = []
        self.name = name #specific name for referencing
        self.code = code #can assign the code if neccesary, but not neccessary
        os.mkdir(self.root)
    def add_subdirectory(self, name, code=None):
        self.subdirectory = Directory(self.root + "/" + name, name, code=code)
        self.subs.append(self.subdirectory)

    def list_subs(self):
        return self.subs

def checkLink(link):
    content = BeautifulSoup(requests.get(link).text, "html.parser")
    blocks = content.find_all(class_="block-container")
    
    for b in blocks:
        if b.find_all(class_="node-body") != []:
            return True
        else:
            return False   

def checkForum(link):
    content = BeautifulSoup(requests.get(link).text, "html.parser")
    struct = content.find(class_="structItemContainer")
    if struct != None:
        return True
    else:
        return False

website = Website("https://www.tortoiseforum.org/", "Tortoise Forum")
directory = Directory("T:/" + website.name + " (" + str(uuid.uuid4())[:8] + ")", "root")

print("Scraping " + website.name)
blocks = website.content.find_all(class_="block-container")
#creates topics
for block in range(len(blocks)):
    if blocks[block].find(class_="block-header--left") != None: #if there is a a block header
        name = str(block) + " " + blocks[block].find(class_="block-header--left").get_text().replace("!", "")[1:-1]
        directory.add_subdirectory(name, blocks[block]) #adds a subdirectory of the name, and the code at the block index
del blocks #I don't know if this works, but I am trying to free up memory

#creates topic subdirectory
for z in range(len(directory.list_subs())):  
    block = directory.list_subs()[z]
    topic = block.code.find_all(class_="node-body") #find all the topic names from within the code
    for t in range(len(topic)):
        title = str(t + 1) + " " + topic[t].find(class_="node-title").get_text().replace("\n", "").replace("?", "")
        link = topic[t].find("a")["href"]
        block.add_subdirectory(title, link) #add a subdirectory to the subdirectory.
'''
    #An example of how a subdirectory can be referenced from a subdirectory and display the "root"(path)
    for i in range(len(block.list_subs())):
        print(block.list_subs()[i].root)
'''
#goes through each topic and determines whether it is a forum or another sub
for z in range(len(directory.list_subs())):
    topics = directory.list_subs()[z].list_subs()
    for i in range(len(topics)):
        link = website.url + topics[i].code[1:]
        if checkLink(link) == True:
            if checkForum(link) == True:
                pass
                #has big titles and forums
            else:
                pass
                #only has the big titles
        else:
            pass
            #only has forums
        

