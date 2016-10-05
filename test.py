#! /usr/bin/env python

from bs4 import BeautifulSoup as Bs
import requests
import re
import os
import sys
import time
import urllib2

wikipedia = 'https://en.wikipedia.org'


def get_links(url, length, depth):
    full_page = requests.get(url)
    full_content = Bs(full_page.text, 'html.parser')

    main_content = full_content.find("div", {"id": "mw-content-text"})
    ignore_div = ['thumb', 'navbox', 'reflist']
    for section in ignore_div:
        for div in main_content.find_all('div', {'class': section}):
            div.decompose()

    for div in main_content.find_all('table', {'class': 'vertical-navbox'}):
        div.decompose()

    wholepage = open('page.html', 'w')
    wholepage.write("%s" % main_content)
    wholepage.close()

    link_count = length
    link_dict = {}

    for sub_link in main_content.find_all('a', attrs={'href': re.compile("/wiki/")}):
        if link_count < 1000:
            link_ref = sub_link.get('href')
            cleaned_link = scrape_link(link_ref)
            if cleaned_link not in link_dict and ':' not in cleaned_link:
                link_dict[cleaned_link] = depth
                link_count += 1

    return link_dict


def scrape_link(dirty_link):
    if '#' in dirty_link:
        position = dirty_link.index('#')
        return dirty_link[0:position]

    return dirty_link


def download_pages(link_list):
    it = 0
    for ind_link in link_list:
        print ind_link
        name = ind_link[6:]
        filename = "%s.html" % name
        com = 'wget %s -O %s' % (wikipedia+ind_link, filename)
        os.system(com)

        # page = requests.get(wikipedia+ind_link)
        # d_page = open(filename, 'w')
        # d_page.write("%s" % page.html)
        # d_page.close()
        # time.sleep(1)
        # it += 1


if __name__ == '__main__':
    i = 0
    depth = 0
    seed = sys.argv[2]
    keyword = sys.argv[2]
    # seed = 'https://en.wikipedia.org/wiki/Sustainable_energy'
    # links = get_links(seed, 0, depth)
    # link_file = open('links_page1.txt', 'w')
    # #
    # while len(links) < 1000:
    #     print wikipedia+links[i], len(links)
    #     links += get_links(wikipedia+links[i], len(links))
    #     print "1 page completed"
    #     i += 1
    # link_file = open('links.txt', 'w')
    # #
    # for link in links:
    #     full_link = wikipedia+link
    #     link_file.write("%s\n" % full_link)
    # link_file.close()


def bfs(seed, keyword):
    bfs_dict = {}
    bfs_dict[seed] = (0, 0)
    return