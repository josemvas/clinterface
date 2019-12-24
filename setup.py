python_requires = (3, 1)

import sys
if sys.version_info < python_requires:
    sys.exit('Python {0} or higher is required to setup this package.'.format('.'.join(str(i) for i in python_requires)))

import setuptools
setuptools.setup()
