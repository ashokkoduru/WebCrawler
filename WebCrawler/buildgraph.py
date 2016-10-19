#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 3rd Oct 2016
# Task   : IR Assignment 1

from bs4 import BeautifulSoup
import requests
import re
import time
import urllib2
from webcrawler import WebCrawler
from datetime import datetime


class GraphBuilder:

    def __init__(self, seed, depth, crawl_type='bfs', keyword=''):
        self.seed = seed
        self.depth = depth
        self.crawl_type = crawl_type
        self.wiki = 'https://en.wikipedia.org'
        self.keyword = keyword
        self.webcrawl = WebCrawler(self.seed, self.depth)

    def crawl_url_bfs(self):
        self.webcrawl.crawler()

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
