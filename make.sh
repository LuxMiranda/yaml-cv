#!/bin/bash

python toLatex.py "$@"
cd tex/moderncv/
xelatex -interaction=batchmode main
cd ../../
cp tex/moderncv/main.pdf CV.pdf
cp CV.pdf ../luxmiranda.github.io/CV.pdf

python toHtml.py
cp html/cv.md ../luxmiranda.github.io/f_cv.md
