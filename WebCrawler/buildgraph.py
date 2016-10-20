#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 15th Oct 2016
# Task   : IR Assignment 2

from webcrawler import WebCrawler
from datetime import datetime
from collections import Counter, deque
import math


class GraphBuilder:

    def __init__(self, seed='', depth=0, d = 0.85):
        self.seed = seed
        self.depth = depth
        self.webcrawl = WebCrawler(self.seed, self.depth)
        self.d = d

    def crawl_url_bfs(self):
        self.webcrawl.crawler()

    def page_rank(self):
        # with open("graph.txt") as f:
        #     page_graph = f.read().splitlines()
        with open("toygraph.txt") as f:
            page_graph = f.read().splitlines()

        graph_dict = self.graph_file_to_dict(page_graph)
        page_rank = {}
        keys_list = []
        values_list = []
        for each in graph_dict:
            keys_list.append(each)
            values_list.extend(graph_dict[each])

        out_links = dict(Counter(values_list))
        print out_links
        values = set(values_list)
        keys = set(keys_list)
        sink_nodes = list(keys - values)
        n = len(graph_dict)
        for each in graph_dict:
            # page_rank[each] = format(1.0/n, '.2f')
            page_rank[each] = 1.0/n
        print page_rank
        p = self.calculate_perplexity(page_rank)
        p_iter = [p, p, p, p]
        print sum(p_iter)
        while sum(p_iter) > 1:
            new_page_rank = {}
            sink_pr = 0
            for s in sink_nodes:
                sink_pr += page_rank[s]
            for p in keys_list:
                new_page_rank[p] = (1-self.d)/float(n)
                new_page_rank[p] += self.d * (float(sink_pr)/n)
                for q in graph_dict[p]:
                    new_page_rank[p] += self.d*(page_rank[p]/out_links[q])
            for p in keys_list:
                page_rank[p] = new_page_rank[p]
            per = self.calculate_perplexity(page_rank)
            p_iter.pop(0)
            p_iter.append(per)
        print page_rank
        prank = sorted(page_rank, key=page_rank.get)
        final_pr = prank[::-1]
        return final_pr

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
        with open("links.txt") as f:
            final_list = f.read().splitlines()
        webcrawl = WebCrawler(self.seed, self.depth)
        link_graph = {}
        counter = 1
        for link in final_list:
            link_graph[link[30:]] = []

        for link in final_list:
            print str(counter) + "----" + link
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
        
    def get_in_links(self, link, final_list):
        print "Inlinks code activated"
        webcrawl = WebCrawler(self.seed, self.depth)
        inlinks = []
        for l in final_list:
            page_links = webcrawl.get_links(l, [])
            if link in page_links:
                inlinks.append(l)
        return inlinks
