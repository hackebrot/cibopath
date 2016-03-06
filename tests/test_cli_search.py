# -*- coding: utf-8 -*-

import pathlib
import json

import pytest


@pytest.fixture
def templates_file():
    return 'tests/templates.json'


def scenarios():
    yield ['django', 'docker'], ['cookiecutter-django']

    yield ['pytest'], [
        'cookiecutter-pylibrary',
        'cookiecutter-pypackage',
        'cookiecutter-pytest-plugin',
    ]
    yield ['api'], ['cookiecutter-tapioca']


@pytest.mark.parametrize('tags, templates', scenarios())
def test_search_templates(cli_runner, tmp_rc, templates_file, tags, templates):
    result = cli_runner([
        '-c', tmp_rc, 'search', '--load-file', templates_file, *tags
    ])

    assert result.exit_code == 0
    for template in templates:
        assert template in result.output
