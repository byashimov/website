#!/usr/bin/env python

import os
import sys

__all__ = {'server', 'makemessages', 'compilemessages'}


def server():
    """
    Runs developer server on 0.0.0.0 with Dev config.
    """

    os.environ['SITE_CONFIG'] = 'website.config.Dev'

    from website import site
    site.run(host='0.0.0.0')


def makemessages():
    """
    Makes translation messages.
    """

    os.system('pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot . '
              '&& pybabel update -i messages.pot -d translations')
    os.unlink('messages.pot')


def compilemessages():
    """
    Compiles translation messages.
    """
    os.system('pybabel compile -d translations')


if __name__ == '__main__':
    # Resolves relative imports
    sys.path.append(os.pardir)

    # Caches for help output
    scope = globals()

    # Returns help if command not on the list
    args = sys.argv[1:]
    if not args or args[0] not in __all__:
        ljust = len(max(__all__, key=len))
        descr = ('{} - {}'.format(fn.ljust(ljust), scope[fn].__doc__.strip())
                 for fn in __all__)
        sys.exit('Available commands:\n' + '\n'.join(descr))

    # Runs command
    scope[args[0]]()
