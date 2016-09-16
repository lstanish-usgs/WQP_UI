#!/bin/bash

echo "You must have python 2.7 and virtualenv installed"
if [ ! -s instance/config.py ]; then
   echo "Please create a instance/config.py file before proceeding. See the README.md for what's required"
   return
fi

if [ "$1" == '--update' ]; then
	echo "Updating npm and bower dependencies";
	npm update;
	bower update;
else
	echo "Installing npm and bower dependencies";
	npm install;
	bower build;
fi

echo "Creating the virtualenv env and installing python requirements"
if [ ! -s env ]; then
    virtualenv --python=python2.7 env
fi
env/bin/pip install -r requirements.txt

echo "Finished installing and building WQP-UI"