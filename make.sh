#!/bin/bash

python toLatex.py "$@"
cd tex/moderncv/
xelatex -interaction=batchmode main
cd ../../
cp tex/moderncv/main.pdf CV.pdf
