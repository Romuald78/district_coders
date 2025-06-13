#!/bin/bash

if ! [  -d "./venv"  ] ; then
   ./create_venv.sh
  if [  $? -ne 0  ] ; then
    exit 1
  fi
fi
source venv/bin/activate
if [  $? -ne 0  ] ; then
  echo "Impossible to activate venv"
fi