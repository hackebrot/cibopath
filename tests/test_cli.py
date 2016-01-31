# -*- coding: utf-8 -*-

from click.testing import CliRunner
import pytest

from cibopath.cli import main

runner = CliRunner()


@pytest.fixture(params=['-V', '--version'])
def version_cli_flag(request):
    return request.param


def test_cli_version(version_cli_flag):
    result = runner.invoke(main, [version_cli_flag])
    assert result.exit_code == 0
    assert result.output.startswith('Cibopath')


def test_option_verbose():
    result = runner.invoke(main, ['-v', 'update'])
    assert result.exit_code == 0
    assert result.output.startswith('DEBUG cli.py: update')


def test_update():
    result = runner.invoke(main, ['update'])
    assert result.exit_code == 0
    assert 'update' in result.output
