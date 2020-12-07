import requests
import uuid
from bs4 import BeautifulSoup
import os
import string
import time
import random

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

def createForum(link, path, title):
    try:
        content = BeautifulSoup(requests.get(link).text, "html.parser")
        if content.find(class_="pageNav-main") != None:
            bar = content.find(class_="pageNav-main").find_all('a')
            last_page = int(bar[-1].get_text())
            del bar

            for page in range(1, last_page + 1):
                newlink = link + "page-" + str(page)
                #print("                " + newlink)
                content = BeautifulSoup(requests.get(newlink).text, "html.parser")
                block = content.find(class_="block-body js-replyNewMessageContainer")
                ##print(link)
                post = block.find_all("article")
                
                f = open(path + "/" + title + ".txt", "a")
                f.write(title + "\n\n")
                for p in post:
                    if p.find(class_="u-anchorTarget") == None:
                        continue
                    header = p.find(class_="message-header").get_text()
                    f.write(formatPosts(header) + "\n")
                    user = p.find(class_="message-cell message-cell--user")
                    user_name = user.find(class_="message-name").get_text()
                    user_title = user.find(class_="userTitle message-userTitle").get_text()
                    f.write(formatPosts(user_name) + " | " + formatPosts(user_title) + "\n")
                    message = p.find(class_="message-cell message-cell--main").find(class_="bbWrapper").get_text()
                    f.write(formatPosts(message) + "\n\n")
        else:
                block = content.find(class_="block-body js-replyNewMessageContainer")
                #print("                " + link)
                post = block.find_all("article")
                
                f = open(path + "/" + title + ".txt", "w")
                f.write(title + "\n\n")
                for p in post:
                    if p.find(class_="u-anchorTarget") == None:
                        continue
                    header = p.find(class_="message-header").get_text()
                    f.write(formatPosts(header) + "\n")
                    user = p.find(class_="message-cell message-cell--user")
                    user_name = user.find(class_="message-name").get_text()
                    user_title = user.find(class_="userTitle message-userTitle").get_text()
                    f.write(formatPosts(user_name) + " | " + formatPosts(user_title) + "\n")
                    message = p.find(class_="message-cell message-cell--main").find(class_="bbWrapper").get_text()
                    f.write(formatPosts(message) + "\n\n")

        f.close()
    except:
        pass

def formatTitle(title):
    title = list(title)
    count = 0
    while count < len(title):
        if title[count] not in string.ascii_letters + string.digits + " ":
            title.pop(count)
            continue
        else:
            count += 1
    title = "".join(title)
    return title

def formatPosts(content):
    
    content = list(content)
    count = 0
    while count < len(content):
        if content[count] not in string.printable:
            content.pop(count)
            continue
        else:
            count += 1
    content = "".join(content)
    return content.replace("\n", "")

def forum(z, i, path):
    try:
        content = BeautifulSoup(requests.get(link).text, "html.parser")
        bar = content.find(class_="pageNav-main").find_all('a')
        last_page = int(bar[-1].get_text())
        del bar
        for page in range(1, last_page + 1):
            newlink = link + "page-" +str(page)
            #print(newlink)
            content = BeautifulSoup(requests.get(newlink).text, "html.parser")
            posts = content.find_all(class_="structItem-title")
            for t in range(len(posts)):
                time.sleep(0.4)
                title = posts[t].get_text()
                title = formatTitle("P" + str(page) + "N" + str(t) + " " + title)
                forum_link = website.url + posts[t].find("a")["href"][1:]
                #print("        " + forum_link)
                path = path.add_subdirectory(title)
                createForum(forum_link, path, title)
    except:
        pass

def randomTime():
    rand = random.randint(100, 500) / 1000
    start = time.time()
    while True:
        if time.time() - rand >= start:
            break
    return


website = Website("https://www.tortoiseforum.org/", "Tortoise Forum")
directory = Directory("T:/" + website.name + " (" + str(uuid.uuid4())[:8] + ")", "root")

#print("Scraping " + website.name)

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
        #print(block.list_subs()[i].root)
'''
#goes through each topic and determines whether it is a forum or another sub
for z in range(len(directory.list_subs())):
    topics = directory.list_subs()[z].list_subs()
    for i in range(len(topics)):
        link = website.url + topics[i].code[1:]
        if checkLink(link) == True:
            if checkForum(link) == True:
                content = BeautifulSoup(requests.get(link).text, "html.parser")
                blocks = content.find_all(class_="block-container")
    
                for b in blocks:
                    nodes = b.find_all(class_="node-body")
                    for n in nodes:
                        link = website.url + n.find("a")["href"]
                        title = formatTitle(n.find(class_="node-title").get_text())
                        directory.list_subs()[z].list_subs()[i].add_subdirectory(title)
                        ##print(title)
                        path = directory.list_subs()[z].list_subs()[i].list_subs()[-1]
                        forum(z, i, path)
                
                path = directory.list_subs()[z].list_subs()[i]
                forum(z, i, path)
            
            else:
                content = BeautifulSoup(requests.get(link).text, "html.parser")
                blocks = content.find_all(class_="block-container")
    
                for b in blocks:
                    nodes = b.find_all(class_="node-body")
                    for n in nodes:
                        link = website.url + n.find("a")["href"]
                        title = formatTitle(n.find(class_="node-title").get_text())
                        directory.list_subs()[z].list_subs()[i].add_subdirectory(title)
                        ##print(title)
                        path = directory.list_subs()[z].list_subs()[i].list_subs()[-1]
                        forum(z, i, path)
        else:
            
            path = directory.list_subs()[z].list_subs()[i]
            forum(z, i, path)
            
