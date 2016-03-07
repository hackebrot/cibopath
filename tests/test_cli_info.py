# -*- coding: utf-8 -*-

import pytest

COOKIECUTTER_DJANGO_INFO = """Name: cookiecutter-django
Author: pydanny
Repository: https://github.com/pydanny/cookiecutter-django
Context: {
    "author_name": "Your Name",
    "description": "A short description of the project.",
    "domain_name": "example.com",
    "email": "Your email",
    "now": "2016/03/05",
    "open_source_license": [
        "MIT",
        "BSD",
        "Not open source"
    ],
    "project_name": "project_name",
    "repo_name": "{{ cookiecutter.project_name|replace(' ', '_') }}",
    "timezone": "UTC",
    "use_celery": "n",
    "use_mailhog": "n",
    "use_newrelic": "n",
    "use_opbeat": "n",
    "use_python2": "n",
    "use_sentry": "n",
    "use_whitenoise": "y",
    "version": "0.1.0",
    "windows": "n",
    "year": "{{ cookiecutter.now[:4] }}"
}
"""


@pytest.fixture
def templates_file():
    return 'tests/templates.json'


def test_template_info(cli_runner, tmp_rc, templates_file):
    result = cli_runner([
        '-c', tmp_rc, 'info',
        '--load-file', templates_file,
        'cookiecutter-django'
        ])
    assert result.exit_code == 0
    assert result.output == COOKIECUTTER_DJANGO_INFO


def test_validate_load_file(cli_runner, tmp_rc):
    result = cli_runner([
        '-c', tmp_rc, 'info',
        '--load-file', 'nope_not_a_file',
        'cookiecutter-django'
        ])
    assert result.exit_code == 1
    assert 'Please run "cibopath update" first.' in result.output
