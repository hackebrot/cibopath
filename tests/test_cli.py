# -*- coding: utf-8 -*-

import configparser

from click.testing import CliRunner
import pytest

from cibopath.cli import main

runner = CliRunner()


@pytest.fixture(params=['-V', '--version'])
def version_cli_flag(request):
    return request.param


def test_version_option(version_cli_flag):
    result = runner.invoke(main, [version_cli_flag])
    assert result.exit_code == 0
    assert result.output.startswith('cibopath')


def test_verbose_option():
    result = runner.invoke(main, ['-v', 'update'])
    assert result.exit_code == 0
    assert result.output.startswith('DEBUG cli.py: update')


def test_update_command():
    result = runner.invoke(main, ['update'])
    assert result.exit_code == 0
    assert 'update' in result.output


@pytest.fixture
def config_file(tmpdir, mocker):
    config_path = tmpdir / 'user_config'
    parser = configparser.RawConfigParser()
    parser['foobar'] = {'hello': 'world'}

    with config_path.open('w', encoding='utf8') as f:
        parser.write(f)

    mocker.patch('cibopath.user_config.USER_CONFIG', config_path)
    return config_path


def test_config_command_list_option(config_file):
    result = runner.invoke(main, ['config', '--list'])
    assert result.exit_code == 0

    assert result.output == '[foobar]\nhello = world\n\n\n'


def test_config_command_variable_value_args(config_file):
    result = runner.invoke(main, ['config', 'abc.def', 'xyz'])
    assert result.exit_code == 0

    config_text = config_file.read_text(encoding='utf8')
    assert config_text == '[foobar]\nhello = world\n\n[abc]\ndef = xyz\n\n'


def test_config_command_variable_validation(config_file):
    result = runner.invoke(main, ['config', 'abc.def.ghi', 'xyz'])
    assert result.exit_code == 2
    assert 'variable needs to be in format section.key' in result.output
