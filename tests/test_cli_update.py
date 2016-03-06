# -*- coding: utf-8 -*-

import pathlib
import json


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
