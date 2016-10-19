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
        with open("links.txt") as f:
            final_list = f.read().splitlines()
        webcrawl = WebCrawler(self.seed, self.depth)
        link_graph = {}

        for link in final_list:
            link_graph[link] = []
            link_graph[link] = []

        for link in final_list:
            page_links = webcrawl.get_links(link, [])
            link_graph[link] = page_links

        for link in final_list:
            print "\n"
            print link
            d = self.get_in_links(link, final_list)
            link_graph[link] = d
            print link_graph[link]

        print link_graph
        print "completed"

    def get_in_links(self, link, final_list):
        print "Inlinks code activated"
        webcrawl = WebCrawler(self.seed, self.depth)
        inlinks = []
        for l in final_list:
            page_links = webcrawl.get_links(l, [])
            if link in page_links:
                inlinks.append(l)
        return inlinks

    def retrieve_doc_id(self, link):
        return

