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
            m_query += math.pow(query_dict[each], 2)

        mag_query = math.sqrt(m_query)
        inv_index = self.ind.build_n_gram_index(1)
        cosine_sim = {}

        for eachfile in glob.glob('*.txt'):
            file_content = open(eachfile)
            content = file_content.read()
            fname = eachfile[:len(eachfile) - 4]
            content = content.split()
            word_count = dict(Counter(content))
            sum_num = 0
            m_doc = 0
            for each in word_count:
                idf_comp = 1+math.log(float(989)/len(inv_index[each]), 10)
                tf_word = word_count[each]/float(len(content))
                m_doc += math.pow(tf_word*idf_comp, 2)
            mag_doc = math.sqrt(m_doc)

            for each_query_term in query_terms:
                if each_query_term in content:
                    tf = word_count[each_query_term]/float(len(content))
                    idf = 1+math.log(float(989)/len(inv_index[each_query_term]), 10)
                    x = tf*idf
                    sum_num += x*query_terms.count(each_query_term)
                else:
                    continue
            denominator = mag_query*mag_doc
            similarity = sum_num/denominator
            cosine_sim[fname] = similarity
        sorted_cosine_dict = sorted(cosine_sim.items(), key=operator.itemgetter(1), reverse=True)
        sorted_cosine_dict = sorted_cosine_dict[:100]
        return sorted_cosine_dict

    def run_query(self, query, queryid):
        print "running query: " + query
        ranked_docs = self.rank_docs_by_query(query)
        os.chdir('..')
        ind = Indexer()
        doc_dict_id = ind.build_docid_dict(ret=True)
        fname = '%s.txt' % query
        f = open(fname, 'w')
        for each in ranked_docs:
            f.write('{} {} {} {} {} {}\n'.format(queryid, 'Q0', each[0], ranked_docs.index(each)+1, each[1],
                                                 'Cosine Similarity'))
        f.close()


def hw4_tasks():
    queries = dict()
    queries['global warming potential'] = 1
    queries['green power renewable energy'] = 2
    queries['solar energy california'] = 3
    queries['light bulb bulbs alternative alternatives'] = 4
    live = True
    r = Retriever()
    print "Welcome to search\n"
    while live:
        query = raw_input('\n\nEnter the query (type exit to end)\n')
        if query == 'exit':
            break
        query_id = queries[query] if query in queries else 0
        r.run_query(query, query_id)
    return

hw4_tasks()
