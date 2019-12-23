import sys
assert sys.version_info >= (3, 0)
from setuptools import setup, find_packages

setup(
    name='bulletin',
    version='0.1.0',
    description='Python prompts made simple.',
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    keywords = "cli prompt",
    author='cronofugo',
    url='https://github.com/cronofugo/python-bulletin',
    license='MIT',
    packages=find_packages(),
    #python_requires=">=2.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    )
