# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages

version = ''
with open('eval_scrubber/__init__.py', 'r') as fp:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fp.read(),
        re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

with open('README.md', 'r') as fp:
    readme = fp.read()
with open('CHANGES.md', 'r') as fp:
    changes = fp.read()
with open('LICENSE.md', 'r') as fp:
    license = fp.read()

setup(
    name='eval_scrubber',
    version=version,
    description='Finds and removes malicious eval base64 PHP code.',
    long_description=readme + '\n\n' + changes,
    author='Eric Bower',
    author_email='neurosnap@gmail.com',
    url='https://github.com/michigan-com/eval_scrubber',
    packages=find_packages(),
    license=license,
    classifiers=(
        b'Development Status :: 3 - Alpha',
        b'Environment :: Console',
        b'Intended Audience :: Developers',
        b'License :: OSI Approved :: MIT License',
        b'Programming Language :: Python :: 2.7',
        b'Programming Language :: Python :: 3.4',
    ),
)
