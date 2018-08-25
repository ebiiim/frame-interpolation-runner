#!/bin/bash

# Usage: sepconv.sh INPUT1 INPUT2 OUTPUT MODEL
# Example: sepconv.sh ./0001.png ./0002.png ./0001z0002.png lf

echo start
cd `dirname $0`
echo `pwd`
ptsc='pytorch-sepconv/'
venv='venv/bin/activate'
echo goto ptsc dir
cd ${ptsc}
echo `pwd`
echo activate venv
source ${venv}
echo run
python run.py --model $4 --first ../$1 --second ../$2 --out ../$3
echo completed
