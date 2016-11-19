#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 16th Nov 2016
# Task   : IR Assignment 4

from indexer import Indexer
from collections import Counter
import os
import glob
import operator
import math

class Retriever:

    def __init__(self):
        self.query = ''
        self.ind = Indexer()
        return

    def rank_docs_by_query(self, query=''):
        self.query = raw_input("Enter the search query\n") if query == '' else query
        query_terms = self.query.lower().split()
        query_dict = dict(Counter(query_terms))
        m_query = 0
        for each in query_dict:
            m_query += query_dict[each]*query_dict[each]
        mag_query = math.sqrt(m_query)
        print mag_query
        inv_index = self.ind.build_n_gram_index(1)
        cosine_sim = {}
        os.chdir('..')
        # doc_dict_id = self.ind.build_docid_dict(ret=True)
        parsed_corpus = os.path.join(os.getcwd(), 'parsed_corpus')
        os.chdir(parsed_corpus)
        for eachfile in glob.glob('*.txt'):
            file_content = open(eachfile)
            content = file_content.read()
            fname = eachfile[:len(eachfile) - 4]
            content = content.split()
            word_count = dict(Counter(content))
            sum_num = 0
            m_doc = 0
            for each_query_term in query_terms:
                if each_query_term in content:
                    tf = word_count[each_query_term]/float(len(content))
                else:
                    continue
                idf = math.log(float(989)/len(inv_index[each_query_term]), 2)
                x = tf*idf
                sum_num += x*query_terms.count(each_query_term)
                m_doc += x*x
            if m_doc != 0:
                mag_doc = math.sqrt(m_doc)
                den = mag_query*mag_doc
                similarity = sum_num/den
                cosine_sim[fname] = similarity
            else:
                cosine_sim[fname] = 0
        sorted_cosine_dict = sorted(cosine_sim.items(), key=operator.itemgetter(1), reverse=True)
        os.chdir('..')
        f = open('cosine_1.txt', 'w')
        for each in sorted_cosine_dict:
            f.write('{} {}\n'.format(each[0], each[1]))
        f.close()


def hw4_tasks():
    r = Retriever()
    queries = dict()
    queries['global warming potential'] = 1
    queries['green power renewable energy'] = 2
    queries['solar energy california'] = 3
    queries['light bulb bulbs alternative alternatives'] = 4
    # r.rank_docs_by_query()
    # l1 = ['a', 'b', 'c']
    # l2 = ['d', 'e']
    # f = open('a.txt', 'a')
    # for i in l1:
    #     f.write(i+'\n')
    # f.close()
    # f = open('a.txt', 'a')
    # for i in l2:
    #     f.write(i + '\n')
    # f.close()


    return

hw4_tasks()
