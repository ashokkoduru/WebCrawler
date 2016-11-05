# Author : Ashok Koduru
# Date   : 2nd Nov 2016
# Task   : IR Assignment 3

from bs4 import BeautifulSoup
import requests
import re
import time
import urllib2
import os
import string

class Indexer:

    def __init__(self):
        return

    def download_pages(self):
        with open('task1_urls.txt') as f:
            links = f.read().splitlines()
        cwd = os.getcwd()
        corpus = os.path.join(cwd, 'corpus')
        parsed_corpus = os.path.join(cwd, 'parsed_corpus')
        if not os.path.exists(corpus):
            os.makedirs(corpus, 0755)
        if not os.path.exists(parsed_corpus):
            os.makedirs(parsed_corpus, 0755)

        i = 1
        for link in links:
            print i, links.index(link)+1, link
            try:
                full_page = requests.get(link)
            except:
                print "Something wrong while requesting the page " + link

            full_content = BeautifulSoup(full_page.text, 'html.parser')
            main_content = full_content.find("div", {"id": "mw-content-text"})
            ignore_div = ['toc', 'thumb', 'navbox', 'reflist']
            for section in ignore_div:
                for div in main_content.find_all('div', {'class': section}):
                    div.decompose()
            for div in main_content.find_all('table', {'class': 'vertical-navbox'}):
                div.decompose()
            for div in main_content.find_all('span', {'class': 'mw-editsection'}):
                div.decompose()
            for div in main_content.find_all('span', {'id': 'References'}):
                div.decompose()
            for div in main_content.find_all('sup'):
                div.decompose()
            parsed_content = self.parse_page(main_content.get_text().encode('utf-8'))
            print type(parsed_content)
            print parsed_content.split()
            return
            docid = link[30:]
            docid = docid.translate(string.maketrans("", ""), string.punctuation)
            # docid = docid.replace('/', '')
            # docid = docid.replace('_', '')
            # docid = docid.replace('-', '')
            filename = "%s.txt" % docid
            fl = open(os.path.join(corpus, filename), 'w')
            fl.write(str(main_content))
            fl.close()
            parsed_fl = open(os.path.join(parsed_corpus, filename), 'w')
            # parsed_fl.write(str(main_content))
            parsed_fl.write(parsed_content)
            parsed_fl.close()
            i += 1

    def parse_page(self, content):

        ignore_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '[', '}', ']', '|',
                       '\\', '"', "'", ';', ':', ',', '.', '/', '<', '>', '?']

        return content.translate(string.maketrans("", ""), string.punctuation)


def hw3_tasks():
    ind = Indexer()
    ind.download_pages()
    # s = "string. With. Punctuation? 5.$$$8"  # Sample string
    # out = s.translate(string.maketrans("", ""), string.punctuation)
    # print os.path.join(os.path.dirname(__file__), 'abc.txt')
    # print out
    return

hw3_tasks()
