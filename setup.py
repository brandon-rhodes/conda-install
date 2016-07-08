# coding: utf-8
"""Install Conda packages right from your requirements.txt file

Do you love the lightning speed with which `Conda`_ installs heavy
binary dependencies like ``numpy`` and ``pandas``, but find yourself
falling back on `pip`_ for more obscure packages?  Is your project setup
split awkwardly between an initial Conda command and a follow-up call to
legacy packaging tools?

With this ``conda-install`` package, you get the best of both worlds!
Your single ``requirements.txt`` file can now list the packages that you
want Conda to install, followed by the other more obscure packages that
you need pip itself to take charge of installing.  Simply write your
``requirements.txt`` file like this::

    conda-install --install-option="numpy scipy pandas"
    skyfield
    jplephem

When this ``conda-install`` package is asked to install, it simply turns
around and asks Conda to install the packages that you listed as its
install options.

History
-------

**1.0** — 2016 July 8 — Initial release.

.. _Conda: http://conda.pydata.org/docs/
.. _pip: https://pip.pypa.io/en/stable/

"""
# Since this package is only designed for use with "pip" anyway, we
# commit the travesty of importing things from `setuptools` instead of
# the standard `distutils` package - because the standard `install`
# command dies when it sees some of the advanced options "pip" supplies.

import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install

open('/tmp/t', 'w').write('{!r}\n'.format(sys.argv))

# The first time pip calls us it invokes the command "egg_info" to learn
# our attributes.  So we wait quietly, and only look for package names
# once we are re-invoked with the "install" command.

if 'install' in sys.argv:

    # We expect that everything past the final `--` option are the
    # package names supplied by `--install-option`.  We go ahead and
    # remove them from `argv` so that `setup()` does not see them and
    # print a command-line usage error.

    i = len(sys.argv)
    while not sys.argv[i-1].startswith('--'):
        i -= 1
    packages_to_install = sys.argv[i:]
    del sys.argv[i:]

# Our custom install behavior: invoking `conda`.

class CondaInstall(install):
    def run(self):
        install.run(self)       # old-fashioned class, so no "super()"
        command = ['conda', 'install', '--yes']
        command.extend(packages_to_install)
        subprocess.check_call(command)

# Finally, our `setup()` stanza.

setup(
    cmdclass={'install': CondaInstall},
    name='conda-install',
    version='1.0',
    description=__doc__.split('\n', 1)[0],
    url='https://github.com/brandon-rhodes/conda-install',
    author='Brandon Rhodes',
    author_email='brandon@rhodesmill.org',
    long_description=__doc__.split('\n', 1)[1],
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
        ),
    )
