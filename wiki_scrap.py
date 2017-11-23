"""Find a connection from one page to another with a minimum of six hops."""
from bs4 import BeautifulSoup
import requests
from queue import deque
import sys


def progressBar(value, endvalue, bar_length=20):
    """Create a progress bar."""
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rlinks:{0} Percent: [{1}] {2}%".format(value, arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def find_wiki_links(wiki_url):
    """Find all links to other wikipedia articles given a wiki url."""
    wiki_connections = list()

    req = requests.get(wiki_url)
    soup = BeautifulSoup(req.content, 'html.parser')

    content_class = {"class": "mw-parser-output"}
    soup = soup.findAll("div", content_class)

    try:
        links = soup[0].findAll('a')
    except IndexError:
        # print("Index error at", soup, wiki_url)
        links = []

    for link in links:
        if 'class' not in link.attrs and link['href'].startswith("/wiki"):
            wiki_connections.append('https://en.wikipedia.org' + link['href'])

    return wiki_connections


def bfs_scrap(root):
    """Scrap wikipedia staring from a given url using breadth first search."""
    graph = dict()
    queue = deque([root])
    seen = set([root])
    level = 0
    total_wikipedia_articles = 5516401

    while queue:
        parent = queue.popleft()
        # a list of the links that the current wikipedia page has
        childs = find_wiki_links(parent)
        graph[parent] = childs

        for node in childs:
            if node not in seen:
                seen.add(node)
                queue.append(node)

        level += 1
        # print(parent)
        # sys.stdout.write("\rlinks checked %i" % level)
        progressBar(level, total_wikipedia_articles)

    return graph


if __name__ == '__main__':
    staring_url = 'https://en.wikipedia.org/wiki/Huffman_coding'
    # wiki_connections = find_wiki_links(staring_url
    graph = bfs_scrap(staring_url)
    # print(graph)
