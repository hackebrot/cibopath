# -*- coding: utf-8 -*-

import logging

import click

from cibopath import __version__


@click.group()
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information', default=False
)
@click.version_option(__version__, u'-V', u'--version', prog_name='Cibopath')
def cli(verbose):
    """Cibopath - Search Cookiecutters on GitHub."""
    if verbose:
        logging.basicConfig(
            format=u'%(levelname)s %(filename)s: %(message)s',
            level=logging.DEBUG
        )
    else:
        logging.basicConfig(
            format=u'%(levelname)s: %(message)s',
            level=logging.INFO
        )


@cli.command('update')
def update_cmd():
    logging.debug('update')
    print('update')

main = cli
