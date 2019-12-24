# Oldest Setuptools version supporting metadata in setup.cfg
setuptools_requires = '30.3.0'

import sys
import setuptools
from distutils.version import StrictVersion
from time import time

# Record time before setup
setup_time = time()

# Setup package if Setuptools is new enough to read metadata from setup.cfg file
if StrictVersion(setuptools.__version__) < StrictVersion(setuptools_requires):
    sys.exit('SetupTools {0} or higher is required to setup this package.'.format(setuptools_requires))
setuptools.setup()

import os
from glob import glob

# Clean generated build and dist-egg files
def rmtree(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            delete_newer(os.path.join(root, f), setup_time, os.remove)
        for d in dirs:
            delete_newer(os.path.join(root, d), setup_time, os.rmdir)
        delete_newer(path, setup_time, os.rmdir)
def delete_newer(node, time, remove):
    if os.path.getctime(node) > time:
        try: remove(node)
        except OSError: pass
rmtree('./build')
for d in glob('./*.egg-info'):
    rmtree(d)

