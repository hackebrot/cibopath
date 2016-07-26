# -*- coding: utf-8 -*-

import logging
import pathlib
import json
import re

import click

from cibopath import __version__
from cibopath.user_config import UserConfig
from cibopath.log import create_logger
from cibopath.scraper import load_templates
from cibopath.templates import dump, load


@click.group()
@click.pass_context
@click.option(
    '-v',
    '--verbose',
    help='Print debug information',
    is_flag=True,
)
@click.option(
    '-c',
    '--config-file',
    default='~/.cibopathrc',
    help='Config file to hold settings',
    type=click.Path(),
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    prog_name='cibopath',
)
def cli(ctx, verbose, config_file):
    """Cibopath - Search Cookiecutters on GitHub."""
    logger = create_logger()
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug('Logger initialized')
    else:
        logger.setLevel(logging.INFO)

    ctx.obj = UserConfig(config_file)


@click.pass_obj
def _templates_file(config):
    try:
        return config.get_value('templates', 'file')
    except KeyError:
        return None


@click.pass_obj
def _username(config):
    try:
        return config.get_value('github', 'username')
    except KeyError:
        return None


@click.pass_obj
def _token(config):
    try:
        return config.get_value('github', 'token')
    except KeyError:
        return None


@cli.command('update')
@click.option(
    '-u',
    '--username',
    default=_username,
    envvar='CIBOPATH_USERNAME',
    required=True,
)
@click.option(
    '-t',
    '--token',
    default=_token,
    envvar='CIBOPATH_TOKEN',
    required=True,
)
@click.option(
    '-d',
    '--dump-file',
    default=_templates_file,
    envvar='CIBOPATH_TEMPLATES_FILE',
    required=True,
    type=click.Path(),
)
def update_cmd(username, token, dump_file):
    logger = logging.getLogger('cibopath')
    logger.debug('username: {}'.format(username))

    logger.debug('token: {}'.format(re.sub(r'\S', '*', token)))

    dump_file = pathlib.Path(dump_file).expanduser()
    dump_file.parent.mkdir(parents=True, exist_ok=True)
    logger.debug('dump_file: {}'.format(dump_file))

    templates = load_templates(username, token)

    logger.debug('Found {} templates'.format(len(templates)))
    dump(templates, dump_file)
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
    '--list',
    'show_config',
    callback=_show_user_config,
    default=False,
    expose_value=False,
    is_eager=True,
    is_flag=True,
)
@click.argument(
    'variable',
    callback=_validate_variable,
)
@click.argument(
    'value',
)
def config_cmd(config, variable, value):
    config.set_value(*variable, value)


def _validate_load_file(ctx, param, value):
    load_file = pathlib.Path(value).expanduser()
    if not load_file.is_file():
        raise click.FileError(
            str(load_file),
            'Please run "cibopath update" first.'
        )
    return load_file


@cli.command('search')
@click.option(
    '-l',
    '--load-file',
    callback=_validate_load_file,
    default=_templates_file,
    required=True,
    type=click.Path(),
)
@click.argument(
    'tags',
    nargs=-1,
    type=click.STRING,
)
def search_cmd(load_file, tags):
    logger = logging.getLogger('cibopath')

    templates = load(load_file)

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


@cli.command('info')
@click.option(
    '-l',
    '--load-file',
    callback=_validate_load_file,
    default=_templates_file,
    required=True,
    type=click.Path(),
)
@click.argument(
    'name',
    type=click.STRING,
)
def info_cmd(load_file, name):
    logger = logging.getLogger('cibopath')

    templates = [t for t in load(load_file) if t.name == name]

    for template in templates:
        logger.debug('Info for {}'.format(template))
        click.echo('Name: {}'.format(template.name))
        click.echo('Author: {}'.format(template.author))
        click.echo('Repository: {}'.format(template.url))

        context = json.dumps(template.context, indent=4, sort_keys=True)
        click.echo('Context: {}'.format(context))


main = cli
