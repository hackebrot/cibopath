# -*- coding: utf-8 -*-

import configparser

import pytest


@pytest.fixture
def config_file(tmpdir):
    config_path = tmpdir / 'user_config'
    parser = configparser.RawConfigParser()
    parser['foobar'] = {'hello': 'world'}

    with config_path.open('w', encoding='utf8') as f:
        parser.write(f)

    return config_path


def test_config_command_list_option(cli_runner, config_file, verbose_cli_flag):
    result = cli_runner([
        verbose_cli_flag, '-c', str(config_file), 'config', '--list'
    ])
    assert result.exit_code == 0

    assert 'DEBUG cibopath cli: Logger initialized' in result.output
    assert 'DEBUG cibopath config: Reading config file' in result.output
    assert '[foobar]\nhello = world\n\n\n' in result.output


def test_config_command_variable_value_args(cli_runner, config_file):
    result = cli_runner([
        '-c', str(config_file), 'config', 'abc.def', 'xyz'
    ])
    assert result.exit_code == 0

    config_text = config_file.read_text(encoding='utf8')
    assert config_text == '[foobar]\nhello = world\n\n[abc]\ndef = xyz\n\n'


def test_config_command_variable_validation(cli_runner, config_file):
    result = cli_runner([
        '-c', str(config_file), 'config', 'abc.def.ghi', 'xyz'
    ])
    assert result.exit_code == 2
    assert 'variable needs to be in format section.key' in result.output
