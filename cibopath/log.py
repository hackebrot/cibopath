# -*- coding: utf-8 -*-

import logging

import click


class ContextFilter(logging.Filter):
    def filter(self, record):
        ctx = click.get_current_context()
        record.cmd = ctx.command.name
        return record


def create_logger():
    logger = logging.getLogger('cibopath')
    logger.setLevel(logging.NOTSET)
    logger.propagate = False
    logger.addFilter(ContextFilter())

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        u'%(levelname)s %(name)s %(cmd)s: %(message)s'
    )
    handler.setFormatter(formatter)

    del logger.handlers[:]
    logger.addHandler(handler)
    return logger
