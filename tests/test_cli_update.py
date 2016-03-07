# -*- coding: utf-8 -*-

import pathlib
import json
from configparser import RawConfigParser

import pytest


def test_store_template_data_to_json(cli_runner, tmp_rc, tmp_templates_file):
    result = cli_runner([
        '-c', tmp_rc, 'update'
    ])

    assert result.exit_code == 0

    templates = pathlib.Path(tmp_templates_file)
    assert templates.exists()

    with templates.open('r', encoding='utf8') as fh:
        template_data = json.load(fh)

    fetched_templates = [template['name'] for template in template_data]
    expected_templates = [
        'cookiecutter-pypackage',
        'cookiecutter-pylibrary',
        'cookiecutter-pytest-plugin',
        'cookiecutter-tapioca',
        'cookiecutter-django',
    ]
    assert fetched_templates == expected_templates


@pytest.fixture
def incomplete_rc(tmpdir):
    rc_file = str(tmpdir / 'noperc')

    config = RawConfigParser()
    config['nope'] = {'foo': 'bar'}

    with open(rc_file, 'w', encoding='utf-8') as fh:
        config.write(fh)
    return rc_file


def test_fail_missing_username(cli_runner, incomplete_rc, tmp_templates_file):
    result = cli_runner([
        '-c', incomplete_rc, 'update',
        '-t', '1234',
        '-d', tmp_templates_file
    ])

    assert result.exit_code == 2
    assert 'Error: Missing option "-u" / "--username".' in result.output
