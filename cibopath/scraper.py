# -*- coding: utf-8 -*-

import asyncio
import logging

import aiohttp

from cibopath import readme_parser, github_api
from cibopath.templates import Template

logger = logging.getLogger('cibopath')

JSON_STORE = 'templates.json'


class CibopathError(Exception):
    """Custom error class for the app."""


class CookiecutterReadmeError(CibopathError):
    """Unable to retrieve readme from github.com/audreyr/cookiecutter."""


class UnableToFindTemplateLinks(CibopathError):
    """Cannot find links to templates in README."""


def fetch_template_data(username, token):
    semaphore = asyncio.Semaphore(10)
    loop = asyncio.get_event_loop()
    auth = aiohttp.BasicAuth(username, token)

    with aiohttp.ClientSession(loop=loop, auth=auth) as client:
        logger.debug('Load Cookiecutter readme')
        cookiecutter_readme = loop.run_until_complete(
            github_api.get_readme(semaphore, client, 'audreyr', 'cookiecutter')
        )
        if not cookiecutter_readme:
            raise CookiecutterReadmeError

        logger.debug('Find GitHub links in Cookiecutter readme')
        github_links, _ = readme_parser.read(cookiecutter_readme)
        if not github_links:
            raise UnableToFindTemplateLinks

        tasks = [
            github_api.get_template(semaphore, client, link)
            for link in github_links
        ]

        logger.debug('Fetch template data from links')
        results = loop.run_until_complete(asyncio.gather(*tasks))
        yield from filter(None, results)  # Ignore all invalid templates


def load_templates(username, token):
    templates = []
    template_data = fetch_template_data(username, token)

    for name, author, repo, context, readme in template_data:
        _, tags = readme_parser.read(readme)
        templates.append(Template(name, author, repo, context, tags))
    return templates
