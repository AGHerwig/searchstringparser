# -*- coding: utf-8 -*-


from __future__ import (absolute_import,)


"""
=============================
Search String Parser Dialects
=============================

:Authors:
    Moritz Emanuel Beber
:Date:
    2015-09-16
:Copyright:
    Copyright |c| 2015, Max Plank Institute for Molecular Genetics, all rights reserved.
:File:
    __init__.py

.. |c| unicode: U+A9
"""


__all__ = ["PostgreSQLTextSearchParser"]


from .postgresql import PostgreSQLTextSearchParser

