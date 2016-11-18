#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 16th Nov 2016
# Task   : IR Assignment 4

from indexer import Indexer
from collections import Counter
from bs4 import BeautifulSoup
import re
import os
import string
import glob
import operator
import math
import matplotlib.pyplot as plt


class Retriever:

    def __init__(self):
        self.query = ''
        self.ind = Indexer()
        return

    def search_query(self):
        self.query = raw_input("Enter the search query\n")
        print self.query.lower().split()

        return

    def rank_docs_by_query(self):
        query_terms = self.query.lower().split()
        cosine_sim = {}
        inv_index = self.ind.build_n_gram_index(1)
        os.chdir('..')
        doc_dict_id = self.ind.build_docid_dict(ret=True)
        for eachdoc in doc_dict_id:
            for each_query_term in query_terms:
                tf = inv_index[each_query_term][doc_dict_id[eachdoc]]
                idf = math.log(float(989)/len(inv_index[each_query_term]), 2)
        return

    def get_idf(self):
        ind = Indexer()
        tf_table = ind.create_tf_table(1, stopword_flag=True)
        (inv_index, tf_dict) = (tf_table[0], tf_table[1])
        total_terms = sum(tf_dict.values())
        print total_terms
        idf = {}
        for each in inv_index:
            i = math.log(float(989) / len(inv_index[each]), 2)
            idf[each] = i
        print idf



def hw4_tasks():
    r = Retriever()
    r.rank_docs_by_query()
    return

hw4_tasks()
