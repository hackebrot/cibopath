# -*- coding: utf-8 -*-

import pathlib
import re
from configparser import RawConfigParser
from functools import partial

import aiohttp
import pytest
from click.testing import CliRunner

from cibopath.cli import main

API_ROOT = 'https://api.github.com/'
GITHUB_REPO = r'(?P<repo>[\w-]+)'
GITHUB_USER = r'(?P<user>[a-zA-Z0-9]+(-[a-zA-Z0-9]+)?)'
SLASH = r'/'

CONTEXT_PATTERN = re.compile(
    API_ROOT + r'repos' + SLASH + GITHUB_USER + SLASH +
    GITHUB_REPO + SLASH + r'contents' + SLASH + r'cookiecutter.json'
)

README_PATTERN = re.compile(
    API_ROOT + r'repos' + SLASH + GITHUB_USER + SLASH +
    GITHUB_REPO + SLASH + r'readme'
)


README_FILES = pathlib.Path('tests/readme_files')
CONTEXT_FILES = pathlib.Path('tests/context_files')


class _Response(aiohttp.ClientResponse):
    def __init__(self, method, url):
        context_match = re.match(CONTEXT_PATTERN, url)
        readme_match = re.match(README_PATTERN, url)

        if context_match:
            context_file = CONTEXT_FILES / '{user}__{repo}'.format(
                **context_match.groupdict()
            )
            self._load_file(context_file)
        elif readme_match:
            readme_file = README_FILES / '{user}__{repo}'.format(
                **readme_match.groupdict()
            )
            self._load_file(readme_file)
        else:
            self._error()

    def _error(self):
        self._return_value = None
        self.status = 404
        self.reason = 'Nope'

    def _success(self, return_value):
        self._return_value = return_value
        self.status = 200
        self.reason = None

    def _load_file(self, file_to_load):
        if file_to_load.exists():
            self._success(file_to_load.read_bytes())
        else:
            self._error()

    async def read(self, *args, **kwargs):
        return self._return_value


class _Client(aiohttp.ClientSession):
    def get(self, url, *args, **kwargs):
        return _Response('get', url)


@pytest.fixture(autouse=True)
def mock_client_session(mocker):
    mocker.patch(
        'cibopath.scraper.aiohttp.ClientSession',
        side_effect=_Client
    )


@pytest.fixture(scope='session')
def cli_runner():
    runner = CliRunner()
    cli_main = partial(runner.invoke, main)
    cli_main.__doc__ = 'Run cibopath cli main'
    return partial(runner.invoke, main)


@pytest.fixture
def tmp_templates_file(tmpdir):
    return str(tmpdir / 'templates.json')


@pytest.fixture
def tmp_rc(tmpdir, tmp_templates_file):
    rc_file = str(tmpdir / 'userrc')

    config = RawConfigParser()
    config['github'] = {
        'username': 'poyo',
        'token': '1234'
    }
    config['templates'] = {
        'file': tmp_templates_file
    }

    with open(rc_file, 'w', encoding='utf-8') as fh:
        config.write(fh)
    return rc_file


@pytest.fixture(params=['-v', '--verbose'])
def verbose_cli_flag(request):
    return request.param
