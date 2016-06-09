# -*- coding: utf-8 -*-


class CibopathException(Exception):
    """Super class for all of Cibopath's exceptions."""


class CookiecutterContextError(CibopathException):
    """Raised when a cookiecutter.json cannot be decoded."""


class GetRequestError(CibopathException):
    """Raised when the status code of a response for a GET request is not 200.
    """
