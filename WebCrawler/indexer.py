# Author : Ashok Koduru
# Date   : 2nd Nov 2016
# Task   : IR Assignment 3

from collections import Counter
from bs4 import BeautifulSoup
import requests
import re
import os
import string
import glob
import operator
import math
import matplotlib.pyplot as plt


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
            print i, links.index(link)+1, link
            if i != links.index(link)+1:
                print "Caught an error while downloading" + link
            try:
                full_page = requests.get(link)
            except:
                print "Something wrong while requesting the page " + link
            full_content = BeautifulSoup(full_page.text, 'html.parser')
            main_content = full_content.find("div", {"id": "mw-content-text"})
            ignore_div = ['toc', 'thumb', 'navbox', 'reflist']
            ignore_table = ['vertical-navbox', 'wikitable']
            ignore_tag = ['sup', 'dl', 'table']
            for section in ignore_div:
                for div in main_content.find_all('div', {'class': section}):
                    div.decompose()
            for section in ignore_table:
                for div in main_content.find_all('table', {'class': section}):
                    div.decompose()
            for section in ignore_tag:
                for div in main_content.find_all(section):
                    div.decompose()
            for div in main_content.find_all('span', {'class': 'mw-editsection'}):
                div.decompose()
            for div in main_content.find_all('span', {'id': 'References'}):
                div.decompose()
            parsed_content = self.parse_page(main_content.get_text().encode('utf-8'))

            docid = link[30:]
            docid = docid.translate(string.maketrans("", ""), string.punctuation)
            filelist.append(docid)
            filename = "%s.txt" % docid
            fl = open(os.path.join(corpus, filename), 'w')
            fl.write(str(main_content))
            fl.close()
            parsed_fl = open(os.path.join(parsed_corpus, filename), 'w')
            parsed_fl.write(parsed_content)
            parsed_fl.close()
            i += 1

    def parse_page(self, content):
        ignore_list = ['!', '@', '#', '$', '^', '&', '*', '(', ')', '_', '+', '=', '{', '[', '}', ']', '|',
                       '\\', '"', "'", ';', ':', '/', '<', '>', '?', '%']
        content = content.translate(None, ''.join(ignore_list))
        content = re.sub("x[a-z][0-9]", "", content)
        content = re.sub("x[0-9]+", "", content)
        content = content.split()
        final_content = ''
        for eachword in content:
            if len(eachword)>1 and eachword[0] == '-':
                eachword = eachword[1:]
            eachword = eachword.lower()
            eachword = eachword.strip('.,-')
            if eachword == '-':
                continue
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
        inverted_index = {}
        token_count = {}
        cwd = os.getcwd()
        parsed_corpus = os.path.join(cwd, 'parsed_corpus')
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
            for token in content_as_list:
                if token not in inverted_index:
                    temp = dict()
                    temp[self.docdict[fname]] = word_count[token]
                    inverted_index[token] = temp
                else:
                    temp = inverted_index[token]
                    temp[self.docdict[fname]] = word_count[token]
                    inverted_index[token] = temp

        return inverted_index

    def create_tf_table(self, n, plot, filesave = True):
        inv_index = self.build_n_gram_index(n)
        tf_dict = {}
        for token in inv_index:
            tf_dict[token] = 0
            for dt in inv_index[token]:
                tf_dict[token] += inv_index[token][dt]
        sorted_tf_dict = sorted(tf_dict.items(), key=operator.itemgetter(1), reverse=True)
        os.chdir("..")
        if plot:
            i = 0
            x = []
            y = []
            for item in sorted_tf_dict:
                i += 1
                x.append(math.log(item[1]))
                y.append(math.log(i))
            plt.title("zipf's law for " + str(n) + " gram inverted index")
            plt.ylabel('term frequency')
            plt.xlabel('rank')
            plt.scatter(x, y)
            plt.show()
        if filesave:
            f = open(str(n)+'_gram_tf_table.txt', 'w')
            for each in sorted_tf_dict:
                f.write('{} {}\n'.format(each[0], each[1]))
            f.close()

    def create_df_table(self, n):
        inv_index = self.build_n_gram_index(n)
        lexic_tokens = sorted(inv_index)
        df_values = []
        for token in lexic_tokens:
            d_lst = []
            for each in inv_index[token]:
                d_lst.append(each)
            df = len(d_lst)
            tup = (token, d_lst, df)
            df_values.append(tup)
        os.chdir("..")
        f = open(str(n)+'_gram_df_table.txt', 'w')
        for each in df_values:
            f.write('{} {} {}\n'.format(each[0], each[1], each[2]))
        f.close()
        # print df_values

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
    # print ind.parse_page(s)
    # print ind.build_n_gram_index(1)
    n = 3
    plot = True
    ind.create_tf_table(n, plot, filesave=False)
    # ind.create_df_table(n)
    return

hw3_tasks()