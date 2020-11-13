import requests
from bs4 import BeautifulSoup
import os
import time

class Direct:
    def __init__(self, root):
        self.root = root
        self.directory = []

    def new_topic(self, topic):
        self.directory.append([topic])

    def find_topic(self, topic):
        return self.directory.index(topic)

    def topic_path(self, index):
        return root + "/" + self.directory[index]

    def new_subtopic(self, topic_index, subtopic):
        self.directory[topic_index].append(subtopic)

    def find_subtopic(self, topic_index, subtopic):
        try:
            return self.directory[topic_index].index(subtopic)
        except:
            return -1
    
    def subtopic_path(self, topic_index, subtopic_index):
        return root + "/" + self.directory[topic_index] + "/" + self.directory[topic_index][subtopic_index]

timestamp = time.time()
link = "https://www.tortoiseforum.org/"

req = requests.get(link) #getting the content
soup = BeautifulSoup(req.text, "html.parser") #gets the whole website
content = soup.find_all(class_="node-body") #gets all major blocks, at least on the front page

pageTitle = soup.find(class_="p-title-value").get_text() #gets the title of the page
root = "T:/" + pageTitle + " " + str(timestamp) #assigns aroot path
os.mkdir(root) #makes root directory
direct = Direct(root) #creates a directory object

block = soup.find_all(class_="block-container") #gets all the major blocks

for b in range(len(block)):
    if block[b].find(class_="block-header--left") != None:
        headerTitle = block[b].find(class_="block-header--left").get_text().replace("!", "")[1:-1]
        direct.new_topic(headerTitle)
        content = block[b].find_all(class_="node-body")
        for c in range(len(content)):
            title = content[c].find(class_="node-title").get_text().replace("\n", "")
            meta = content[c].find(class_="node-meta").get_text().replace("\n\n\n", " ").replace("\n", "~")
            info = title + " " + meta
            print(direct.directory)
            direct.new_subtopic(direct.find_topic([headerTitle]), [info])
            
