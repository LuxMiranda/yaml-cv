#!/bin/bash

git add .
git commit -m "Update"
git push origin main

cd ../luxmiranda.github.io
git add .
git commit -m "Update CV"
git push origin main
