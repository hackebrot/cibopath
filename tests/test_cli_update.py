# -*- coding: utf-8 -*-

import pathlib


def test_should_write_json(cli_runner, tmp_rc, tmp_templates_file):
    result = cli_runner([
        '-c', tmp_rc, 'update'
    ])

    assert result.exit_code == 0

    templates = pathlib.Path(tmp_templates_file)
    assert templates.exists()
