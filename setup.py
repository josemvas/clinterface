python_requires = (3, 1)

# Check if python version is high enough
import sys
if sys.version_info < python_requires:
    sys.exit('Python {0} or higher is required to setup this package.'.format('.'.join(str(i) for i in python_requires)))

# Record setup starting time
import time
setup_time = time.time()

# Setup package with setup.cfg options
import setuptools
setuptools.setup()

# Clean generated build and dist-egg files
import os
import glob
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
for d in glob.glob('./*.egg-info'):
    rmtree(d)

