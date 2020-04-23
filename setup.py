 #!/usr/bin/env python
# yapf

import os
import kingston
import tempfile
import subprocess

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install = (
    "funcy>=1.10.2",
    "pysistence>=0.4.1",
    "patterns>=0.3",
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
long_desc = ''
try:
    tmpdir = tempfile.mkdtemp()
    outpath = os.path.join(tmpdir, 'kingston-README.rst')
    subprocess.check_call(['pandoc', 'README.org', '-o', outpath])
    with open(outpath) as fp:
        long_desc = fp.read()
except Exception:
    long_desc = ''  # nothing to do.

setup(
    name='kingston',
    cmdclass=cmdclass,
    version=kingston.__version__,
    description="Some Python nicieties",
    long_description=long_desc,
    packages=('kingston', ),
    author='Jacob Oscarson',
    author_email='jacob@414soft.com',
    install_requires=install,
    tests_require=install+develop,
    extras_require={
        'test': install + develop,
    },
    url='https://www.414soft.com/kingston',
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
