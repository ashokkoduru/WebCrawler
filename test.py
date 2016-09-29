from bs4 import BeautifulSoup as bs
import requests

url = 'https://en.wikipedia.org/wiki/Sustainable_energy'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
links = open('links.txt', 'w')
match = '/wiki/'
ignore = [':', '#']
link_count = 0
depth = 1

link_list = []
for link in soup.find_all('a'):
    link_list.append(link.lstrip(link.rstrip()))
    links.write("%s\n" % link.get('href'))
    link_count += 1

