# -*- coding: utf-8 -*-

import json
import logging
import pathlib

GITHUB_URL = 'https://github.com/{user}/{repo}'

TEMPLATE_DIR = pathlib.Path.home() / '.cibopath'
TEMPLATE_DIR.mkdir(exist_ok=True)

JSON_STORE = TEMPLATE_DIR / 'templates.json'

logger = logging.getLogger('cibopath')


class Template:
    def __init__(self, name, author, repo, context, tags):
        self.name = name
        self.author = author
        self.repo = repo
        self.context = context
        self.tags = tags

    def __repr__(self):
        return '<Template {name}>'.format(name=self.name)

    def __contains__(self, tag):
        return tag in self.tags

    @property
    def url(self):
        return GITHUB_URL.format(user=self.author, repo=self.repo)


def template_to_json(python_object):
    if isinstance(python_object, Template):
        return {
            '__class__': 'Template',
            'name': python_object.name,
            'author': python_object.author,
            'repo': python_object.repo,
            'context': python_object.context,
            'tags': python_object.tags,
        }
    raise TypeError


def template_from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'Template':
            author = json_object['author']
            name = json_object['name']
            repo = json_object['repo']
            context = json_object['context']
            tags = json_object['tags']
            return Template(name, author, repo, context, tags)
    return json_object


def dump(templates, file_path=JSON_STORE):
    logger.debug('Dumping templates to {}'.format(file_path))
    with file_path.open('w', encoding='utf8') as f:
        json.dump(templates, f, default=template_to_json)


def load(file_path=JSON_STORE):
    logger.debug('Loading templates from {}'.format(file_path))
    with file_path.open('r', encoding='utf8') as f:
        return json.load(f, object_hook=template_from_json)
