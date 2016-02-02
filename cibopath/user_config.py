# -*- coding: utf-8 -*-

import configparser
import logging
import pathlib

USER_CONFIG = pathlib.Path.home() / '.cibopathrc'


def get_text():
    logging.debug('Reading config file {}'.format(USER_CONFIG))
    return USER_CONFIG.read_text(encoding='utf8')


def read_config():
    logging.debug('Loading config file {}'.format(USER_CONFIG))
    config = configparser.RawConfigParser()

    with USER_CONFIG.open('r', encoding='utf8') as config_file:
        config.read_file(config_file)
    return config


def set_value(section, key, value):
    config = read_config()

    logging.debug(
        'Set config key "{key}" of section "{section}" to "{value}"'
        ''.format(key=key, section=section, value=value)
    )

    if section not in config.sections():
        config[section] = {}
    config[section][key] = value

    with USER_CONFIG.open('w', encoding='utf8') as config_file:
        config.write(config_file)
