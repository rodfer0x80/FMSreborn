#!/bin/sh
rm -rf ./venv ./src/__pycache__ ./src/*/__pycache__ ./debug.log
ls ./ | grep -E '^[0-9]+' | xargs rm -rf 
