# -*- coding: utf-8 -*-

import re
from html.parser import HTMLParser

START = r'^'
SLASH = r'/'
GITHUB_BASE = r'https://github\.com'
GITHUB_USER = r'(?P<user>[a-zA-Z0-9]+(-[a-zA-Z0-9]+)?)'
GITHUB_REPO = r'(?P<repo>[\w-]+)'
END = r'$'

GITHUB_LINK = re.compile(
    START + GITHUB_BASE + SLASH +
    GITHUB_USER + SLASH +
    GITHUB_REPO + END
)

WORD = re.compile(r'\b([a-zA-Z0-9]+(?:[\.\-][a-zA-Z0-9]+)*)\b')


class ReadmeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._words = set([])
        self.in_link = False
        self.in_list_item = False

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.in_list_item = True
            return

        if not self.in_list_item:
            return

        for link in [val for name, val in attrs if name == 'href']:
            match = re.match(GITHUB_LINK, link)
            if not match:
                continue

            self.in_link = True
            self.links.append(match.groupdict())

    def handle_endtag(self, tag):
        if tag == 'a' and self.in_link:
            self.in_link = False

        elif tag == 'li' and self.in_list_item:
            self.in_list_item = False

    def handle_data(self, data):
        self._words.update(re.findall(WORD, data))

        if not self.in_list_item or not self.in_link:
            return
        self.links[-1].update({'name': data})

    @property
    def words(self):
        return [word.lower() for word in self._words]


def read(string):
    parser = ReadmeParser()
    parser.feed(string)
    return parser.links, parser.words
