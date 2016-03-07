# -*- coding: utf-8 -*-

from click.testing import CliRunner
import pytest

from cibopath.cli import main
from cibopath import __version__

runner = CliRunner()


@pytest.fixture(params=['-V', '--version'])
def version_cli_flag(request):
    return request.param


def test_cli_group_version_option(version_cli_flag):
    result = runner.invoke(main, [version_cli_flag])
    assert result.exit_code == 0
    assert result.output == 'cibopath, version {}\n'.format(__version__)
