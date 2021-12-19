#!/bin/bash

python setup.py test sdist bdist_wheel
twine check dist/*
twine upload dist/*

rm -rf dist build *.egg-info