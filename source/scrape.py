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
    def __init__(self, root, name, code=None, parent=None):
        self.root = root
        self.subs = []
        self.name = name
        self.code = code
        os.mkdir(self.root)
    def add_subdirectory(self, name, code=None):
        self.subdirectory = Directory(self.root + "/" + name, name, code=code)
        self.subs.append(self.subdirectory)

    def list_subs(self):
        return self.subs

website = Website("https://www.tortoiseforum.org/", "Tortoise Forum")
directory = Directory("T:/" + website.name + " (" + str(uuid.uuid4())[:8] + ")", "root")

print("Scraping " + website.name)
blocks = website.content.find_all(class_="block-container")
for block in blocks:
    if block.find(class_="block-header--left") != None:
        name = block.find(class_="block-header--left").get_text().replace("!", "")[1:-1]
        directory.add_subdirectory(name, block)

for z in range(len(directory.list_subs())):
    block = directory.list_subs()[z].code
    topic = block.find_all(class_="node-body")
    for t in range(len(topic)):
        title = str(t + 1) + " " + topic[t].find(class_="node-title").get_text().replace("\n", "").replace("?", "")
        print(title)
