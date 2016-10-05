#! /usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re
import sys
import time
import urllib2


class WebCrawler:

    def __init__(self, seed, depth, crawl_type='bfs'):
        self.seed = seed
        self.depth = depth
        self.crawl_type = crawl_type
        self.wiki = 'https://en.wikipedia.org'

    def crawler(self):
        if self.crawl_type == 'bfs':
            self.crawl_bfs()

        return

    def crawl_dfs(self):
        final_list = []

        def crawl(link):
            if link in final_list:
                return
            url_list = self.get_links(link, final_list)
            final_list.append(self.seed)
            for link in url_list:
                crawl(link)
            crawl(self.seed)
        return final_list

    def crawl_bfs(self):
        print 'inside'
        url_list = []
        final_list = []
        url_list.append(self.seed)
        crawl_depth = 0

        while crawl_depth < self.depth+1 and url_list:
            if self.crawl_type == 'bfs':
                print "bfs"
                link = url_list.pop(0)
            else:
                print 'dfs'
                link = url_list.pop()
            print link
            crawled_links = self.get_links(link, final_list)
            for each_link in crawled_links:
                url_list.append(each_link)
                final_list.append(each_link)
            crawl_depth += 1

        link_file = open('links.txt', 'w')

        for link in final_list:
            link_file.write("%s\n" % link)
        link_file.close()

    def get_links(self, link, link_list):
        links = []
        try:
            full_page = requests.get(link)
        except:
            print "Something wrong while requesting the page"
            return link_list

        full_content = BeautifulSoup(full_page.text, 'html.parser')

        main_content = full_content.find("div", {"id": "mw-content-text"})
        ignore_div = ['thumb', 'navbox', 'reflist']
        for section in ignore_div:
            for div in main_content.find_all('div', {'class': section}):
                div.decompose()
        for div in main_content.find_all('table', {'class': 'vertical-navbox'}):
            div.decompose()

        link_count = len(link_list)
        parsed_content = main_content.find_all('a', attrs={'href': re.compile("/wiki/")})

        for sub_link in parsed_content:
            if link_count < 1000:
                link_ref = sub_link.get('href')
                cleaned_link = self.scrape_link(link_ref)
                if self.wiki+cleaned_link not in link_list and ':' not in cleaned_link:
                    links.append(self.wiki+cleaned_link)
                    link_count += 1

        return links

    def scrape_link(self, dirty_link):
        if '#' in dirty_link:
            position = dirty_link.index('#')
            return dirty_link[0:position]
        return dirty_link

