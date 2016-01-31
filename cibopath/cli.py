# -*- coding: utf-8 -*-

import click

from cibopath import __version__


@click.group()
@click.version_option(__version__, u'-V', u'--version', prog_name='Cibopath')
def cli():
    """Cibopath - Search Cookiecutters on GitHub."""


@cli.command('update')
def update_cmd():
    print('update')

main = cli
