# Author : Ashok Koduru
# Date   : 2nd Nov 2016
# Task   : IR Assignment 3

from collections import Counter
from bs4 import BeautifulSoup
import requests
import re
import time
import urllib2
import os
import string
import glob
import operator

class Indexer:
    def __init__(self):
        self.docdict = {}
        return

    def download_pages(self):
        with open('task1_urls.txt') as f:
            links = f.read().splitlines()
        cwd = os.getcwd()
        corpus = os.path.join(cwd, 'corpus')
        filelist = []
        parsed_corpus = os.path.join(cwd, 'parsed_corpus')
        if not os.path.exists(corpus):
            os.makedirs(corpus, 0755)
        if not os.path.exists(parsed_corpus):
            os.makedirs(parsed_corpus, 0755)

        i = 1
        for link in links:
            # link = links[0]
            # print i, links.index(link)+1, link
            # if i != links.index(link)+1:
            #     print "Caught an error while downloading" + link
            # try:
            #     full_page = requests.get(link)
            # except:
            #     print "Something wrong while requesting the page " + link
            #
            # full_content = BeautifulSoup(full_page.text, 'html.parser')
            # main_content = full_content.find("div", {"id": "mw-content-text"})
            # ignore_div = ['thumb', 'navbox', 'reflist']
            # for section in ignore_div:
            #     for div in main_content.find_all('div', {'class': section}):
            #         div.decompose()
            # for div in main_content.find_all('table', {'class': 'vertical-navbox'}):
            #     div.decompose()
            # for div in main_content.find_all('span', {'class': 'mw-editsection'}):
            #     div.decompose()
            # for div in main_content.find_all('span', {'id': 'References'}):
            #     div.decompose()
            # for div in main_content.find_all('sup'):
            #     div.decompose()
            # parsed_content = self.parse_page(main_content.get_text().encode('utf-8'))

            docid = link[30:]
            docid = docid.translate(string.maketrans("", ""), string.punctuation)
            filelist.append(docid)
        filelist_set = set(filelist)
        print len(filelist_set), len(filelist)
        return
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
        ignore_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '[', '}', ']', '|',
                       '\\', '"', "'", ';', ':', '/', '<', '>', '?']
        # print content
        content = content.translate(None, ''.join(ignore_list))
        content = content.split()
        print content
        # print content
        final_content = ''
        # print content
        for eachword in content:
            eachword = eachword.strip('.,')
            if eachword == '-':
                eachword = ''
            final_content += eachword + ' '
        return final_content

    def build_docid_dict(self):
        with open('task1_urls.txt') as f:
            links = f.read().splitlines()
        counter = 1
        for link in links:
            docid = link[30:]
            docid = docid.translate(string.maketrans("", ""), string.punctuation)
            self.docdict[docid] = counter
            counter += 1

    def build_n_gram_index(self, n):
        self.build_docid_dict()
        one_gram_index = {}
        token_count = {}
        cwd = os.getcwd()
        parsed_corpus = os.path.join(cwd, 'test')
        os.chdir(parsed_corpus)
        for eachfile in glob.glob('*.txt'):
            print eachfile
            file_content = open(eachfile)
            content = file_content.read()
            fname = eachfile[:len(eachfile) - 4]
            content_as_list = content.split()
            if n != 1:
                content_as_list = self.find_ngrams(content_as_list, n)
            if n == 1:
                token_count[fname] = len(content_as_list)
            else:
                token_count[fname] = 0
            word_count = dict(Counter(content_as_list))
            # print word_count
            # print "dfdsfdsfdsf"
            for token in content_as_list:
                if token not in one_gram_index:
                    temp = dict()
                    temp[eachfile] = word_count[token]
                    one_gram_index[token] = temp
                else:
                    temp = one_gram_index[token]
                    temp[eachfile] = word_count[token]
                    one_gram_index[token] = temp

        return one_gram_index

    def create_tf_table(self, n):
        inv_index = self.build_n_gram_index(n)
        tf_dict = {}
        for token in inv_index:
            tf_dict[token] = 0
            for dt in inv_index[token]:
                tf_dict[token] += inv_index[token][dt]
        print tf_dict
        sorted_tf_dict = sorted(tf_dict.items(), key=operator.itemgetter(1), reverse=True)
        os.chdir("..")
        f = open('tf_table.txt', 'w')
        for each in sorted_tf_dict:
            f.write('{}.....................{}\n'.format(each[0], each[1]))
        f.close()

    def find_ngrams(self, input_list, n):
        zip_list = zip(*[input_list[i:] for i in range(n)])
        gram_list = []
        for each in zip_list:
            m = list(each)
            m = ' '.join(m)
            gram_list.append(m)
        return gram_list

def hw3_tasks():
    ind = Indexer()
    # ind.download_pages()
    # s = "string. With. Punctuation? \n \n \n 5.8 wit.h 3,200"  # Sample string
    # print ind.parse_page(s)
    # ind.build_n_gram_index(3)
    ind.create_tf_table(1)
    # return
    # m = {}
    # tl = {'a': {1: 4, 2: 7, 4:7}, 'b': {3: 5, 2: 4}}
    # for i in tl:
    #     m[i] = 0
    #     for j in tl[i]:
    #         m[i] += tl[i][j]
    # print m
    # a = ['a', 'b', 'c', 'a', 'd', 'c', 'e']
    # input_list = ['all', 'this', 'happened', 'more', 'or', 'less']
    # l = ind.find_ngrams(input_list, 2)
    # print l
    # a = [('the', 542), ('of', 487), ('and', 422), ('to', 279), ('engineering', 258)]
    # for each in a:
    #     print each[0], each[1]
    return

hw3_tasks()
