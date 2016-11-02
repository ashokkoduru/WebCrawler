#! /usr/bin/env python

# Author : Ashok Koduru
# Date   : 2nd Nov 2016
# Task   : IR Assignment 3

from bs4 import BeautifulSoup
import requests
import re
import time
import urllib2


class Indexer:

    def __init__(self):
        return

    def download_pages(self):
        with open('task1_urls.txt') as f:
            links = f.read().splitlines()
        print links

def hw3_tasks():
    return

hw3_tasks()