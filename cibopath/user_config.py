# -*- coding: utf-8 -*-

import configparser
import logging
import pathlib

logger = logging.getLogger('cibopath')


class UserConfig:
    def __init__(self, file_path):
        self.file_path = pathlib.Path(file_path).expanduser()
        self.file_path.touch(exist_ok=True)
        self._config = self._load_config()

    @property
    def text(self):
        logger.debug('Reading config file {}'.format(self.file_path))
        return self.file_path.read_text(encoding='utf8')

    def _load_config(self):
        logger.debug('Loading config file {}'.format(self.file_path))
        config = configparser.RawConfigParser()

        with self.file_path.open('r', encoding='utf8') as config_file:
            config.read_file(config_file)
        return config

    def set_value(self, section, key, value):
        logger.debug(
            'Set config key "{key}" of section "{section}" to "{value}"'
            ''.format(key=key, section=section, value=value)
        )

        if section not in self._config.sections():
            self._config[section] = {}
        self._config[section][key] = value

        with self.file_path.open('w', encoding='utf8') as config_file:
            self._config.write(config_file)

    def get_value(self, section, key):
        logger.debug(
            'Get config key "{key}" of section "{section}"'
            ''.format(key=key, section=section)
        )
        return self._config[section][key]
