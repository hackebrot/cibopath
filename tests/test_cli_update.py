# -*- coding: utf-8 -*-

import json
import pathlib
from configparser import RawConfigParser

import pytest

from cibopath.cli import load_templates, dump


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


def test_fail_missing_token(cli_runner, incomplete_rc, tmp_templates_file):
    result = cli_runner([
        '-c', incomplete_rc, 'update',
        '-u', 'chew',
        '-d', tmp_templates_file
    ])

    assert result.exit_code == 2
    assert 'Error: Missing option "-t" / "--token".' in result.output


def test_fail_missing_dump_file(cli_runner, incomplete_rc):
    result = cli_runner([
        '-c', incomplete_rc, 'update',
        '-u', 'chew',
        '-t', '1234'
    ])

    assert result.exit_code == 2
    assert 'Error: Missing option "-d" / "--dump-file".' in result.output


@pytest.fixture
def mock_load(mocker):
    return mocker.patch(
        'cibopath.cli.load_templates',
        autospec=True,
        side_effect=load_templates,
    )


@pytest.fixture
def mock_dump(mocker):
    return mocker.patch(
        'cibopath.cli.dump',
        autospec=True,
        side_effect=dump,
    )


def test_credentials_from_env(
        cli_runner, mock_load, mock_dump, monkeypatch, tmp_templates_file):
    monkeypatch.setenv('CIBOPATH_USERNAME', 'user1234')
    monkeypatch.setenv('CIBOPATH_TOKEN', '1234')
    monkeypatch.setenv('CIBOPATH_TEMPLATES_FILE', tmp_templates_file)

    result = cli_runner([
        '--verbose',
        'update',
    ])
    assert result.exit_code == 0

    assert mock_load.call_args == [('user1234', '1234')]

    dump_templates_file = str(mock_dump.call_args[0][1])
    assert dump_templates_file == tmp_templates_file
