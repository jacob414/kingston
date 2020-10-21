# yapf
import sys
import os
import tempfile
import subprocess
import glob


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
    for org in glob.glob('*.org'):
        name, *_ = org.split('.org')
        with open(f"docs/{name.lower()}.rst", 'w') as rst:
            rst.write(
                os.linesep.join(
                    (f".. _{name.lower()}:", "", org_2_rst(f"{name}.org"))))


if __name__ == '__main__':
    if '--convert-from-org' in sys.argv:
        convert_from_org()
    else:
        print("kingston.build: use --readme-from-org to examd org-mode files"
              "into Sphinx docs")
