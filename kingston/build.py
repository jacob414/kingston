# yapf
import sys
import os
import tempfile
import subprocess


def readme_2_rst():
    try:
        tmpdir = tempfile.mkdtemp()
        outpath = os.path.join(tmpdir, 'kingston-README.rst')
        subprocess.check_call(['pandoc', 'README.org', '-o', outpath])
        with open(outpath) as fp:
            return fp.read()
    except Exception as exc:
        print(exc)
        return ''  # nothing to do.


def readme_from_org():
    with open('docs/readme.rst', 'w') as fp:
        fp.write(os.linesep.join((
            '.. _readme:', '',
            readme_2_rst())))


if __name__ == '__main__':
    if '--readme-from-org' in sys.argv:
        readme_from_org()
    else:
        print("kingston.build: use --readme-from-org to examd README.org"
              "into Sphinx docs")
