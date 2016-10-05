#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 3rd Oct 2016
# Task   : IR Assignment 1

from bs4 import BeautifulSoup
import requests
import re
import sys
import time
import urllib2


class WebCrawler:

    def __init__(self, seed, depth, crawl_type='bfs', keyword=''):
        self.seed = seed
        self.depth = depth
        self.crawl_type = crawl_type
        self.wiki = 'https://en.wikipedia.org'
        self.keyword = keyword

    def crawler(self):
        if self.crawl_type == 'bfs':
            self.crawl_bfs()
        elif self.crawl_type == 'dfs':
            self.crawl_dfs()

    def crawl_dfs(self):
        print 'inside dfs'
        final_list = []
        depth = self.depth

        def crawl(link, d):
            if link in final_list:
                return
            url_list = self.get_links(link, final_list)
            final_list.append(self.seed)

            for link in url_list:
                crawl(link)
            crawl(self.seed, depth)
        return final_list

    def dfs_limit(self, link, finish_list):
        url_list = [link]
        depth = self.depth
        if link in finish_list:
            return finish_list
        path = []

        while url_list:
            current_link = url_list.pop()

            # if current_link in finish_list:
            #     path.append(current_link)
            #     return path

            if link in url_list:
                # finished this level; go back up one level
                depth += 1
                path.pop()

            elif depth != 0:
                # go one level deeper, push sentinel
                depth -= 1
                path.append(current_link)
                url_list.append(link)
                url_list.extend(self.get_links(link, path))

    def crawl_bfs(self):
        print 'inside'
        url_list = []
        final_list = []
        url_list.append(self.seed)
        current_depth = 0
        timetodepthincrease = len(url_list)

        while current_depth < self.depth and url_list and len(final_list) < 1000:
            link = url_list.pop(0)
            timetodepthincrease -= 1
            if timetodepthincrease == 0:
                current_depth += 1
                pending_depth_increase = True
            print link, len(final_list)
            crawled_links = self.get_links(link, final_list)
            for each_link in crawled_links:
                url_list.append(each_link)
                final_list.append(each_link)
                if pending_depth_increase:
                    pending_depth_increase = False
                    timetodepthincrease = len(url_list)

        link_file = open('links.txt', 'w')

        for link in final_list:
            link_file.write("%s\n" % link)
        link_file.close()

    def get_links(self, link, link_list):
        links = []
        output = link_list
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
        parsed_content = main_content.find_all('a', attrs={'href': re.compile("^/wiki/")})

        for sub_link in parsed_content:
            if link_count < 1000:
                link_ref = sub_link.get('href')
                cleaned_link = self.scrape_link(link_ref)
                not_duplicate = self.wiki+cleaned_link not in output
                not_admin = ':' not in cleaned_link
                matched = True
                if self.keyword != '':
                    cleaned_link_key = cleaned_link[6:]
                    matched = self.keyword.lower() in cleaned_link_key.lower()
                if not_duplicate and not_admin and matched:
                    print cleaned_link
                    links.append(self.wiki+cleaned_link)
                    link_count += 1
        return links

    def scrape_link(self, dirty_link):
        if '#' in dirty_link:
            position = dirty_link.index('#')
            return dirty_link[0:position]
        return dirty_link

