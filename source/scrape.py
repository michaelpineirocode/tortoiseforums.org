import requests
import uuid
from bs4 import BeautifulSoup
import os

class Website:
    def __init__(self, url, name):
        self.url = url
        self.name = name

class Directory:
    def __init__(self, root, parent=None):
        self.root = root
        self.subs = []
        os.mkdir(self.root)
    def add_subdirectory(self, name):
        self.subdirectory = Directory(self.root + "/" + name, self)
        self.subs.append(self.subdirectory)

    def list_subs(self):
        return self.subs

website = Website("https://www.tortoiseforum.org/", "Tortoise Forum")
directory = Directory("T:/" + website.name + " (" + str(uuid.uuid4())[:8] + ")")
directory.add_subdirectory("test root")
print(directory.list_subs()[0].root)
