#!/bin/bash
export PYTHONPATH="$PYTHONPATH:/usr/lib/python2.7/site-packages"

cd /root/data/DFCF_TRADER
/usr/bin/python2 -u app.py > log.txt 2>&1 &
