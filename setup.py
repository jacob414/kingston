 #!/usr/bin/env python
# yapf

import os
import kingston
from kingston import build

import tempfile
import subprocess

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install = (
    "funcy>=1.10.2",
    "jsonpickle>=1.2",
)  # yapf: disable

develop = (
    "pytest>=5.0.1",
    "hypothesis>=4.24.3",
    "altered_states>=1.0.9",
    "pycodestyle>=2.5.0",
    "mypy>=0.770",
    "pyflakes>=2.1.1",
    "flake8",
)  # yapf: disable

try:
    # make setup.py review available only to fully dev-capable
    # interpreter instances
    import mypy
    assert mypy

    from kingston.testing import ReviewProject
    cmdclass = {'review': ReviewProject}
except ImportError:
    cmdclass = {}

# Try to convert README to RST using pandoc (allowed to fail).

setup(
    name='kingston',
    cmdclass=cmdclass,
    version=kingston.__version__,
    description="Some Python nicieties",
    long_description=build.org_2_rst('README.org'),
    packages=('kingston', ),
    author='Jacob Oscarson',
    author_email='jacob@414soft.com',
    install_requires=install,
    tests_require=install+develop,
    extras_require={
        'test': install + develop,
    },
    package_data = {
        'kingston': ['py.typed'],
    },
    url='https://github.com/jacob414/kingston',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
