#!/bin/bash

pip install .[build] && \
pip install .[test] && \
python setup.py sdist bdist_wheel && \
twine check dist/* && \
pytest && \
twine upload dist/*

rm -rf dist build *.egg-info