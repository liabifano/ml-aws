#!/usr/bin/env
set -e

ENVPATH=$(dirname $(dirname `realpath $0`))/modelapp-python-env/
echo $ENVPATH

if [ -d $ENVPATH ]; then rm -rf $ENVPATH; fi

virtualenv -p python3 $ENVPATH
echo " --- virtualenv in $ENVPATH --- "
echo " --- activate virtualenv --- "

cd $(dirname $(dirname `realpath $0`))/modelapp/

source $ENVPATH/bin/activate
pip3 install -e .
deactivate
