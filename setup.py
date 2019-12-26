# Minimum Setuptools version supporting configuration metadata in setup.cfg
#min_stversion = '30.3'
# Minimum Setuptools version supporting conditional python dependencies (PEP 508)
min_stversion = '32.2'

import sys
import setuptools
from time import time

# Record time before setup
setup_time = time()

# Setup package if Setuptools version is high enough
setuptools.setup(setup_requires=['setuptools>=' + min_stversion])

import os
from glob import glob
#from shutil import rmtree

# Delete only files generated after setup
def rmtree(path):
    def delete_newer(node, time, delete):
        if os.path.getctime(node) > time:
            try: delete(node)
            except OSError as e: print(e)
    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            delete_newer(os.path.join(root, f), setup_time, os.remove)
        for d in dirs:
            delete_newer(os.path.join(root, d), setup_time, os.rmdir)
    delete_newer(path, setup_time, os.rmdir)

rmtree('./build')
for d in glob('./*.egg-info'):
    rmtree(d)

