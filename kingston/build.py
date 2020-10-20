# yapf
import sys
import os
import tempfile
import subprocess


def org_2_rst(orgsrc):
    name, *_ = orgsrc.split('.org')
    name = name.lower()
    try:
        tmpdir = tempfile.mkdtemp()
        outpath = os.path.join(tmpdir, f'kingston-{name}.rst')
        subprocess.check_call(['pandoc', orgsrc, '-o', outpath])
        with open(outpath) as fp:
            return fp.read()
    except Exception as exc:
        print(exc)
        return ''  # nothing to do.


def convert_from_org():
    with open('docs/readme.rst', 'w') as fp:
        fp.write(os.linesep.join((
            '.. _readme:', '',
            org_2_rst('README.org'))))
    with open('docs/changelog.rst', 'w') as fp:
        fp.write(os.linesep.join((
            '.. _changelog:', '',
            org_2_rst('CHANGELOG.org'))))


if __name__ == '__main__':
    if '--convert-from-org' in sys.argv:
        convert_from_org()
    else:
        print("kingston.build: use --readme-from-org to examd README.org"
              "into Sphinx docs")
