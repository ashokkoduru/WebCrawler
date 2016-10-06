#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 3rd Oct 2016
# Task   : IR Assignment 1

from bs4 import BeautifulSoup
import requests
import re
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

    def crawl_dfs_recursion(self):
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

    # def crawl_dfs(self, link, depth):
    #     depth = 1
    #
    #     if depth > self.depth:
    #         return
    #     if self.seed in :
    #         return
    #
    #     links = self.get_links(self.seed)
    #     self.crawl_dfs(link[0])
    #     depth += 1

    def crawl_bfs(self):
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
            time.sleep(1)
            for each_link in crawled_links:
                url_list.append(each_link)
                final_list.append(each_link)
                if pending_depth_increase:
                    pending_depth_increase = False
                    timetodepthincrease = len(url_list)

        link_file = open('links.txt', 'w')

        if self.keyword == '':
            final_list.insert(0, self.seed)
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
                not_duplicate_local = self.wiki+cleaned_link not in output
                not_duplicate_final = self.wiki + cleaned_link not in links
                not_admin = ':' not in cleaned_link
                matched = True
                if self.keyword != '':
                    cleaned_link_key = cleaned_link[6:]
                    matched = self.keyword.lower() in cleaned_link_key.lower()
                if not_duplicate_final and not_duplicate_local and not_admin and matched:
                    # print cleaned_link
                    links.append(self.wiki+cleaned_link)
                    link_count += 1
        return links

    def scrape_link(self, dirty_link):
        if '#' in dirty_link:
            position = dirty_link.index('#')
            return dirty_link[0:position]
        return dirty_link

    def download_pages(self, list):
        for each in list:
            response = urllib2.urlopen(list)
            html = response.read()
            # page = open()