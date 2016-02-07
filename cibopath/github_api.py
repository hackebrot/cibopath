# -*- coding: utf-8 -*-

import base64
import logging
import json

import aiohttp

logger = logging.getLogger('cibopath')

API_ROOT = 'https://api.github.com/'
API_README = API_ROOT + 'repos/{user}/{repo}/readme'
API_COOKIECUTTER_JSON = (
    API_ROOT + 'repos/{user}/{repo}/contents/cookiecutter.json'
)

async def get(client, url, *, headers=None):
    if headers is None:
        headers = {}

    async with client.get(url, headers=headers) as response:
        assert response.status == 200, response.reason + url
        content = await response.read()
        return content.decode()


async def get_cookiecutter_json(semaphore, client, user, repo):
    headers = {'Accept': 'application/json'}
    url = API_COOKIECUTTER_JSON.format(user=user, repo=repo)

    async with semaphore:
        with aiohttp.Timeout(10):
            content = await get(client, url, headers=headers)
            json_content = json.loads(content)
            decoded = base64.b64decode(json_content['content']).decode()
            return json.loads(decoded)


async def get_readme(semaphore, client, user, repo):
    headers = {'Accept': 'application/vnd.github.V3.html+json'}
    url = API_README.format(user=user, repo=repo)

    async with semaphore:
        with aiohttp.Timeout(10):
            html_content = await get(client, url, headers=headers)
            return html_content


async def get_template(semaphore, client, link):
    user = link['user']
    name = link['name']
    repo = link['repo']

    logger.debug('{}/{} GET'.format(user, repo))
    try:
        logger.debug('{}/{} JSON'.format(user, repo))
        cookiecutter_json = await get_cookiecutter_json(
            semaphore, client, user, repo
        )
        logger.debug('{}/{} README'.format(user, repo))
        readme = await get_readme(semaphore, client, user, repo)
    except AssertionError:
        logger.debug('{}/{} FAIL'.format(user, repo))
        return False
    else:
        logger.debug('{}/{} SUCCESS'.format(user, repo))
        return name, user, repo, cookiecutter_json, readme
