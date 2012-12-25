#!/bin/bash

ROOT_DIR=`cd \`dirname "$0"\`; pwd`

cd $ROOT_DIR
echo $ROOT_DIR

which pip
if [ "$?" == "1" ]; then
    brew install python
    pip install virtualenv
fi

which virtualenv
if [ "$?" == "1" ]; then
    echo $PATH | grep -q -s "/usr/local/share/python"
    if [ $? -eq 1 ] ; then
        PATH=/usr/local/share/python:$PATH
        export PATH
    fi
fi

virtualenv venv
source venv/bin/activate

pip install WebTest
