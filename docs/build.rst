Build
=====

These are instructions for how to develop, build and deploy Blue Dot.

Develop
-------

Install / upgrade tools::

    sudo python3 -m pip install --upgrade pip setuptools wheel twine virtualenv

Create a virtual environment (recommended)::

    virtualenv --system-site-packages bluedot-dev
    cd bluedot-dev
    source bin/activate 

Clone repo and install for dev::

    git clone https://github.com/martinohanlon/BlueDot
    cd BlueDot
    git checkout dev
    python3 setup.py develop

Test
----

Install `pytest`_::

    pip3 install -U pytest

Run tests::

    cd BlueDot/tests
    pytest -v

Deploy
------

Build for deployment::

    python3 setup.py sdist
    python3 setup.py bdist_wheel
    python setup.py bdist_wheel

Deploy to `PyPI`_::

    twine upload dist/* --skip-existing


.. _pytest: https://doc.pytest.org/
.. _PyPI: https://pypi.python.org/pypi
