try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A program to help figure out object pixel positions',
    'author': 'Collin McLean',
    'url': 'http://github.com/wingedillidan/PosTool',
    'author_email': 'wingedillidan@gmail.com',
    'version': '0.1.2',
    'install_requires': ['nose'],
    'packages': ['PosTool'],
    'scripts': [],
    'name': 'PosTool'
}

setup(**config)
