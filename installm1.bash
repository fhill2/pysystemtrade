#!/bin/bash
# rm -rf .venv
# pyenv local 3.8.17
# python -m venv .venv
# source .venv/bin/activate

# NOTE: 
pip uninstall cython -y
pip install cython==0.29.20
# might have to remove all these dependencies from setup.py or pyproject.toml
OPENBLAS="$(brew --prefix openblas)" MACOSX_DEPLOYMENT_TARGET=$(sw_vers -productVersion | cut -d. -f1,2) python -m pip install cython --no-use-pep517

OPENBLAS="$(brew --prefix openblas)" MACOSX_DEPLOYMENT_TARGET=$(sw_vers -productVersion | cut -d. -f1,2) python -m pip install "numpy>=1.19.4,<1.24.0" --no-use-pep517

OPENBLAS="$(brew --prefix openblas)" MACOSX_DEPLOYMENT_TARGET=$(sw_vers -productVersion | cut -d. -f1,2) python -m pip install pandas==1.0.5 --no-use-pep517

OPENBLAS="$(brew --prefix openblas)" MACOSX_DEPLOYMENT_TARGET=$(sw_vers -productVersion | cut -d. -f1,2) python -m pip install scipy --no-use-pep517

OPENBLAS="$(brew --prefix openblas)" MACOSX_DEPLOYMENT_TARGET=$(sw_vers -productVersion | cut -d. -f1,2) python -m pip install statsmodels==0.12.2 --no-use-pep517

OPENBLAS="$(brew --prefix openblas)" MACOSX_DEPLOYMENT_TARGET=$(sw_vers -productVersion | cut -d. -f1,2) python -m pip install PyYAML==5.3 --no-use-pep517
#  --no-use-pep517
# 


pip install -r ./requirementsm1.txt \
    && python ./setupm1.py develop
