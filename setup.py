import sys
from setuptools import setup

if sys.version_info[0] == 2:
    if not sys.version_info >= (2, 7):
        raise ValueError('This package requires Python 2.7 or newer')
elif sys.version_info[0] == 3:
    if not sys.version_info >= (3, 3):
        raise ValueError('This package requires Python 3.3 or newer')
else:
    raise ValueError('Unrecognized major version of Python')

__project__ = 'bluedot'
__desc__ = 'A zero boiler plate bluetooth remote'
__version__ = '1.2.3'
__author__ = "Martin O'Hanlon"
__author_email__ = 'martin@ohanlonweb.com'
__license__ = 'MIT'
__url__ = 'https://github.com/martinohanlon/BlueDot'
__requires__ = ['pydbus',]

__classifiers__ = [
#   "Development Status :: 3 - Alpha",
#   "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: Communications",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
]

if __name__ == '__main__':
    setup(name='bluedot',
          version = __version__,
          description = __desc__,
          url = __url__,
          author = __author__,
          author_email = __author_email__,
          license= __license__,
          packages = [__project__],
          #install_requires = __requires__,
          entry_points={
              'console_scripts': [
                  'bluedotapp = bluedot.app:main'
                  ]},
          zip_safe=False)
