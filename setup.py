from setuptools import setup

__project__ = 'bluedot'
__desc__ = 'A zero boiler plate bluetooth remote'
__version__ = '1.0.1'
__author__ = "Martin O'Hanlon"
__author_email__ = 'martin@ohanlonweb.com'
__license__ = 'MIT'
__url__ = 'https://github.com/martinohanlon/BlueDot'
__requires__ = ['pydbus',]

__classifiers__ = [
#    "Development Status :: 3 - Alpha",
#    "Development Status :: 4 - Beta",
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

setup(name='bluedot',
      version = __version__,
      description = __desc__,
      url = __url__,
      author = __author__,
      author_email = __author_email__,
      license= __license__,
      packages = [__project__],
#      install_requires = __requires__,
      zip_safe=False)
