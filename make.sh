#!/bin/bash

python toLatex.py "$@"
cd tex
xelatex -interaction=batchmode main
cd ../
cp tex/main.pdf CV.pdf
