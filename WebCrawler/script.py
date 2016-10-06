from webcrawler import WebCrawler

# x = WebCrawler('https://en.wikipedia.org/wiki/Solar_power', 5, 'bfs')
x = WebCrawler('https://en.wikipedia.org/wiki/Sustainable_energy', 5, 'bfs', 'solar')
# x.get_links('https://en.wikipedia.org/wiki/Sustainable_energy', [])

x.crawler()
