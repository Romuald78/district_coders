#!/bin/bash
python3 -m venv venv
if [  $? -ne 0  ] ; then
  echo "Impossible to create venv"
  exit 1
fi
./venv/bin/python -m pip install --upgrade pip
if [  $? -ne 0  ] ; then
  echo "Impossible to upgrade pip"
  exit 1
fi
./venv/bin/python -m pip install --upgrade setuptools
if [  $? -ne 0  ] ; then
  echo "Impossible to upgrade setuptools"
  exit 1
fi
./venv/bin/python -m pip install -r requirements.txt
if [  $? -ne 0  ] ; then
  echo "Impossible to install requirements.txt"
  exit 1
fi
