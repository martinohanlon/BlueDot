Build instructions
==================

These are instructions for how to develop, build and deploy Blue Dot.

bluedot python library
----------------------

Setup
~~~~~

Clone repo and install for dev::

    git clone https://github.com/martinohanlon/BlueDot
    cd BlueDot/bluedot
    git checkout dev
    sudo python3 setup.py develop

Test
~~~~

Install pytest::

    sudo pip3 install -U pytest

Run tests::

    cd BlueDot/tests
    pytest -v

Deploy
~~~~~~

Create .pypirc credentials file::

    nano ~/.pypirc

    [distutils]
    index-servers =
        pypi

    [pypi]
    username:
    password:    

Build for deployment::

    python3 setup.py sdist

Deploy to pypi::

    twine upload dist/* --skip-existing