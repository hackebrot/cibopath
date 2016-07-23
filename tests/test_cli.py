# -*- coding: utf-8 -*-

import pytest

from cibopath import __version__


@pytest.fixture(params=['-V', '--version'])
def version_cli_flag(request):
    return request.param


def test_cli_group_version_option(cli_runner, version_cli_flag):
    result = cli_runner([version_cli_flag])
    assert result.exit_code == 0
    assert result.output == 'cibopath, version {}\n'.format(__version__)
