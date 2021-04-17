#!/usr/bin/env bash

function setup_venv() {
    conda deactivate
    deactivate
    rm -rf venv
    python -m venv venv
    venv/bin/activate
}

function pip_compile() {
  pip-compile -r requirements/build.in
  pip-compile -r requirements/docs.in
  pip-compile -r requirements/tests.in
  pip-compile -r requirements/dev.in
  . scripts/script_get_python_requirements_from_txt.sh
  pip check
}

function pip_install() {
  pip install -r requirements/build.in
  pip install -r requirements/docs.in
  pip install -r requirements/tests.in
  pip install -r requirements/dev.in
  pip check
}

function pip_install_via_setup_py() {
  python setup.py develop
  pip install -e .
  pip check
}

function build_wheel() {
  python -m pip install --upgrade pip
  pip install setuptools wheel twine
  python setup.py sdist bdist_wheel
  python -m build --wheel
  pip check
}

function main() {
  # setup_venv
  pip_compile
  pip_install
  pip_install_via_setup_py
  #build_wheel
}

main
