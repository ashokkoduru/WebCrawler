#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 15th Oct 2016
# Task   : IR Assignment 2

from webcrawler import WebCrawler
from datetime import datetime
from collections import Counter
import math
import operator


class GraphBuilder:

    def __init__(self, pagerank_file, graph_file='links.txt', seed='', depth=0, d=0.85):
        self.seed = seed
        self.depth = depth
        self.webcrawl = WebCrawler(self.seed, self.depth)
        self.d = d
        self.graph_file_name = graph_file
        self.page_rank_file = pagerank_file

    def page_rank(self):
        with open(self.page_rank_file) as f:
            page_graph = f.read().splitlines()

        graph_dict = self.graph_file_to_dict(page_graph)
        page_rank = {}
        keys_list = []
        values_list = []
        for each in graph_dict:
            keys_list.append(each)
            values_list.extend(graph_dict[each])
            # if(len(graph_dict[each]) == 0):
            #     print each

        out_links = dict(Counter(values_list))
        values = set(values_list)
        keys = set(keys_list)
        sink_nodes = list(keys - values)
        n = len(graph_dict)
        for each in graph_dict:
            page_rank[each] = 1.0/n
        px = self.calculate_perplexity(page_rank)
        counter_diff = 0
        loop_counter = 1
        px_values = []
        while counter_diff < 5:
            px_values.append(px)
            new_page_rank = {}
            sink_pr = 0
            for s in sink_nodes:
                sink_pr += page_rank[s]
            for p in keys_list:
                new_page_rank[p] = (1-self.d)/n
                new_page_rank[p] += self.d*sink_pr/n
                for q in graph_dict[p]:
                    new_page_rank[p] += self.d*page_rank[q]/out_links[q]
            for p in keys_list:
                page_rank[p] = new_page_rank[p]
            new_px = self.calculate_perplexity(page_rank)
            print px - new_px
            if px - new_px < 1:
                counter_diff += 1
                # print "Here"
            else:
                counter_diff = 0
            px = new_px
            loop_counter += 1
        print px_values
        prank = sorted(page_rank, key=page_rank.get)
        sorted_pr = sorted(page_rank.items(), key=operator.itemgetter(1), reverse=True)
        px_file = open('G1_perplexity_values.txt', 'w')
        i = 1
        for e in px_values:
            px_file.write("The perplexity for round {} is  ---  {}\n".format(i, e))
            i += 1
        px_file.close()
        return sorted_pr

    def calculate_perplexity(self, pagerank):
        ent = 0
        for each in pagerank:
            ent += float(pagerank[each])*math.log(float(pagerank[each]), 2)
        entropy = 0 - ent
        perplexity = math.pow(2, entropy)
        return perplexity

    def graph_file_to_dict(self, graph):
        graph_dict = {}
        for node in graph:
            listl = node.split()
            graph_dict[listl[0]] = listl[1:]
        return graph_dict

    def build_graph(self):
        print str(datetime.now())
        with open(self.graph_file_name) as f:
            final_list = f.read().splitlines()
        webcrawl = WebCrawler(self.seed, self.depth)
        link_graph = {}
        counter = 1
        for link in final_list:
            link_graph[link[30:]] = []

        for link in final_list:
            print str(counter) + " --- " + link
            page_links = webcrawl.get_links(link, [])
            common_links = list(set(page_links).intersection(final_list))
            for c_link in common_links:
                link_graph[c_link[30:]].append(link[30:])
            counter += 1
        graph_file = open('graph.txt', 'w')

        for link in link_graph:
            graph_file.write("%s %s\n" % (link, " ".join(link_graph[link])))
        graph_file.close()

        print "completed"
        print str(datetime.now())


def tasks_hw2():
    filename1 = 'toygraph.txt'
    filename2 = 'G1.txt'
    filename3 = 'wt2g_inlinks.txt'
    x = GraphBuilder(filename2)
    # x.build_graph()
    pagerank = x.page_rank()
    return


tasks_hw2()