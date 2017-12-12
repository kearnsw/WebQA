from setuptools import setup, find_packages
import sys

if sys.version_info < (3,):
    sys.exit('Medhelp requires Python 3.')

with open('requirements.txt') as f:
    reqs = f.read()

setup(
        name='medhelp',
        version='0.0.1',
        description='tools for extraction of terms from medhelp',
        url='https://github.com/kearnsw/medhelp',
        license='GPLv3.0',
        packages=find_packages(exclude=('notebooks')),
        install_requires=reqs.strip().split('\n'),

)
