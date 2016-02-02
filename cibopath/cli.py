# -*- coding: utf-8 -*-

import logging

import click

from cibopath import __version__
from cibopath import user_config


@click.group()
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information', default=False
)
@click.version_option(__version__, u'-V', u'--version', prog_name='cibopath')
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


def _show_user_config(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(user_config.get_text())
    ctx.exit()


def _validate_variable(ctx, param, value):
    try:
        section, key = value.split('.')
        return section, key
    except ValueError:
        raise click.BadParameter('variable needs to be in format section.key')


@cli.command('config')
@click.option(
    '--list', 'show_config', is_flag=True, default=False,
    is_eager=True, expose_value=False, callback=_show_user_config
)
@click.argument('variable', callback=_validate_variable)
@click.argument('value')
def config_cmd(variable, value):
    user_config.set_value(*variable, value)

main = cli
