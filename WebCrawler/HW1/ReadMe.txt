I Wrote a class for WebCrawler which is webcrawler.py

It has 4 arguments

1. url to be crawled
2. depth till which it should be crawled
3. type of crawl, this is an optional parameter. It could be either 'bfs' or 'dfs'. bfs is the default option
4. Key word to be matched against url. It is also optional

Steps to run the program. Go to the folder which has the webcrawler.py file.

from webcrawler import WebCrawler

For Task 1
x = WebCrawler('https://en.wikipedia.org/wiki/Sustainable_energy', 5,)

For Task 2 BFS
x = WebCrawler('https://en.wikipedia.org/wiki/Sustainable_energy', 5, 'bfs', 'solar')

For Task 3
x = WebCrawler('https://en.wikipedia.org/wiki/Solar_power', 5, 'bfs')

Calling the carwler on the constructed object
x.crawler()
