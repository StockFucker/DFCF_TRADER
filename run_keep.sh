#!/bin/bash
export PYTHONPATH="$PYTHONPATH:/usr/lib/python2.7/site-packages"

cd /root/data/DFCF_TRADER
/usr/bin/python2 -u keep_alive.py > log2.txt 2>&1 &
