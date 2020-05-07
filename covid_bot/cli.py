"""
Module that contains the command line app.
Why does this file exist, and why not put this in __main__
  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:
  - When you run `python -mcsci_utils` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``csci_utils.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``csci_utils.__main__`` in ``sys.modules``.
  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
from luigi import build

from .xtract import XmlParser
from .datafetch import ContentHtml, ContentBotTemplate


def main():  # pragma: no cover
    build(
        [ContentHtml(),
         ContentBotTemplate()
         ],
        local_scheduler=True)

    xmlparser = XmlParser(["cdcfaq", ])
    xmlparser.extactIntents(4)
    xmlparser.generateexcelforanalyst()
    xmlparser.generatebot()