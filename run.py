#!/usr/bin/env python

import os
import sys

__all__ = {'server', 'makemessages', 'compilemessages', 'tests'}


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)


def server():
    """
    Runs developer server on 0.0.0.0 with Dev config.
    """

    os.environ['SITE_CONFIG'] = 'website.config.Dev'

    from website import site
    site.run(host='0.0.0.0')


def tests():
    """
    Runs tests and reports coverage.
    """

    os.environ['SITE_CONFIG'] = 'website.config.Testing'
    os.system('coverage run -m unittest discover -t {} -s {} '
              '&& coverage report'
              .format(PARENT_DIR, ROOT_DIR))


def makemessages():
    """
    Makes translation messages.
    """

    pot = os.path.join(ROOT_DIR, 'messages.pot')
    translations = os.path.join(ROOT_DIR, 'translations')
    babel = os.path.join(ROOT_DIR, 'babel.cfg')

    # Creates translations
    os.system('pybabel -q extract --omit-header -s --no-location '
              '-k lazy_gettext -F {babel} -o {pot} {root} '
              '&& pybabel update -i {pot} -d {translations}'
              .format(root=ROOT_DIR, babel=babel, pot=pot,
                      translations=translations))

    # Removes pot file
    os.unlink(pot)

    # Removes meta data
    for root, dirs, files in os.walk(translations):
        pos = (f for f in files if f.endswith('.po'))
        for po in pos:
            path = os.path.join(root, po)
            with open(path, 'r') as trans:
                clean = (
                    s for s in trans.readlines()
                    # --omit-header doesn't work :(
                    if not s.startswith(('"', '#', 'msgid ""', 'msgstr ""'))
                )

            with open(path, 'w+') as trans:
                trans.writelines(''.join(clean).strip())


def compilemessages():
    """
    Compiles translation messages.
    """

    translations = os.path.join(ROOT_DIR, 'translations')
    os.system('pybabel compile -d ' + translations)


if __name__ == '__main__':
    # Resolves relative imports
    sys.path.append(PARENT_DIR)

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
