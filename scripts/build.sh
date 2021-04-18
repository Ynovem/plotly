#!/usr/bin/env bash

cd "$(dirname "${0}")/.." || exit

#pipenv run pip freeze > requirements.txt

docker build -t test .

#rm requirements.txt
