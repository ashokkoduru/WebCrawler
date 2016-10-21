from webcrawler import WebCrawler
from buildgraph import GraphBuilder

# x = WebCrawler('https://en.wikipedia.org/wiki/Solar_power', 5, 'bfs')
y = WebCrawler('https://en.wikipedia.org/wiki/Sustainable_energy', 5)
# x.get_links('https://en.wikipedia.org/wiki/Sustainable_energy', [])

x = GraphBuilder('links.txt')

# x.crawl_url_bfs()
# print y.get_links('https://en.wikipedia.org/wiki/Sustainable_energy', [])[2]
#x.build_graph()
a = x.page_rank()
print a
