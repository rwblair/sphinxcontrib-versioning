#!/usr/bin/env python
"""Setup script for the project."""

from __future__ import print_function

import codecs
import os
import re

from setuptools import Command, setup

IMPORT = 'sphinxcontrib.versioning'
INSTALL_REQUIRES = ['click', 'colorclass', 'sphinx']
LICENSE = 'MIT'
NAME = 'sphinxcontrib-versioning'
VERSION = '2.2.1'


def readme(path='README.rst'):
    """Try to read README.rst or return empty string if failed.

    :param str path: Path to README file.

    :return: File contents.
    :rtype: str
    """
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    handle = None
    url_prefix = 'https://raw.githubusercontent.com/Robpol86/{name}/v{version}/'.format(name=NAME, version=VERSION)
    try:
        handle = codecs.open(path, encoding='utf-8')
        return handle.read(131072).replace('.. image:: docs', '.. image:: {0}docs'.format(url_prefix))
    except IOError:
        return ''
    finally:
        getattr(handle, 'close', lambda: None)()


class CheckVersion(Command):
    """Make sure version strings and other metadata match here, in module/package, tox, and other places."""

    description = 'verify consistent version/etc strings in project'
    user_options = []

    @classmethod
    def initialize_options(cls):
        """Required by distutils."""
        pass

    @classmethod
    def finalize_options(cls):
        """Required by distutils."""
        pass

    @classmethod
    def run(cls):
        """Check variables."""
        project = __import__(IMPORT, fromlist=[''])
        for expected, var in [('@Robpol86', '__author__'), (LICENSE, '__license__'), (VERSION, '__version__')]:
            if getattr(project, var) != expected:
                raise SystemExit('Mismatch: {0}'.format(var))
        # Check changelog.
        if not re.compile(r'^%s - \d{4}-\d{2}-\d{2}[\r\n]' % VERSION, re.MULTILINE).search(readme()):
            raise SystemExit('Version not found in readme/changelog file.')
        # Check tox.
        if INSTALL_REQUIRES:
            contents = readme('tox.ini')
            section = re.compile(r'[\r\n]+install_requires =[\r\n]+(.+?)[\r\n]+\w', re.DOTALL).findall(contents)
            if not section:
                raise SystemExit('Missing install_requires section in tox.ini.')
            in_tox = re.findall(r'    ([^=]+)==[\w\d.-]+', section[0])
            if INSTALL_REQUIRES != in_tox:
                raise SystemExit('Missing/unordered pinned dependencies in tox.ini.')


if __name__ == '__main__':
    setup(
        author='@Robpol86',
        author_email='robpol86@gmail.com',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Framework :: Sphinx :: Extension',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: MacOS',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Documentation :: Sphinx',
            'Topic :: Software Development :: Documentation',
        ],
        cmdclass=dict(check_version=CheckVersion),
        description='Sphinx extension that allows building versioned docs for self-hosting.',
        entry_points={'console_scripts': ['sphinx-versioning = sphinxcontrib.versioning.__main__:cli']},
        install_requires=INSTALL_REQUIRES,
        keywords='sphinx versioning versions version branches tags',
        license=LICENSE,
        long_description=readme(),
        name=NAME,
        package_data={'': [
            os.path.join('_static', 'banner.css'),
            os.path.join('_templates', 'banner.html'),
            os.path.join('_templates', 'layout.html'),
            os.path.join('_templates', 'versions.html'),
        ]},
        packages=['sphinxcontrib', os.path.join('sphinxcontrib', 'versioning')],
        url='https://github.com/Robpol86/' + NAME,
        version=VERSION,
        zip_safe=False,
        namespace_packages=['sphinxcontrib'],
    )
