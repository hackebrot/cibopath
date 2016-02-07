# -*- coding: utf-8 -*-

import logging
import operator

import click

from cibopath import __version__
from cibopath.user_config import UserConfig
from cibopath.log import create_logger
from cibopath.scraper import load_templates
from cibopath.templates import dump, load


@click.group()
@click.pass_context
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information'
)
@click.option(
    '-c', '--config-file',
    type=click.Path(), default='~/.cibopathrc',
    help='Config file to hold settings'
)
@click.version_option(__version__, u'-V', u'--version', prog_name='cibopath')
def cli(ctx, verbose, config_file):
    """Cibopath - Search Cookiecutters on GitHub."""
    ctx.obj = UserConfig(config_file)

    logger = create_logger()
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug('Logger initialized')
    else:
        logger.setLevel(logging.INFO)


@click.pass_obj
def _default_username(config):
    try:
        return config.get_value('github', 'username')
    except KeyError:
        return None


@click.pass_obj
def _default_token(config):
    try:
        return config.get_value('github', 'token')
    except KeyError:
        return None


@cli.command('update')
@click.option('-u', '--username', required=True, default=_default_username)
@click.option('-t', '--token', required=True, default=_default_token)
def update_cmd(username, token):
    logger = logging.getLogger('cibopath')
    logger.debug(
        'username:{username} token:{token}'
        ''.format(username=username, token=token)
    )
    templates = load_templates(username, token)

    logger.debug('Found {} templates'.format(len(templates)))
    dump(templates)
    logger.debug('Successfully updated templates')


def _show_user_config(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(ctx.obj.text)
    ctx.exit()


def _validate_variable(ctx, param, value):
    try:
        section, key = value.split('.')
        return section, key
    except ValueError:
        raise click.BadParameter('variable needs to be in format section.key')


@cli.command('config')
@click.pass_obj
@click.option(
    '--list', 'show_config', is_flag=True, default=False,
    is_eager=True, expose_value=False, callback=_show_user_config
)
@click.argument('variable', callback=_validate_variable)
@click.argument('value')
def config_cmd(config, variable, value):
    config.set_value(*variable, value)


@cli.command('search')
@click.argument('tags', type=click.STRING, nargs=-1)
def search_cmd(tags):
    logger = logging.getLogger('cibopath')

    try:
        templates = load()
    except FileNotFoundError as err:
        logger.error(
            'Unable to load templates. '
            'Please run "cibopath update" first.'
        )
        return

    matches = []
    for template in templates:
        logger.debug('Processing {}'.format(template))

        if all(tag.lower() in template for tag in tags):
            matches.append(template)

    if not matches:
        click.echo('No match for "{}"'.format(', '.join(tags)))
        return

    message = '{template.name:.<36} {template.url}'
    for match in sorted(matches):
        click.echo(message.format(template=match))


main = cli
