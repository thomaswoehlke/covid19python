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
  pip install -r requirements/build.in  --log logfile1.txt
  pip install -r requirements/docs.in  --log logfile2.txt
  pip install -r requirements/tests.in --log logfile3.txt
  pip install -r requirements/dev.in --log logfile4.txt
  pip check
}

function pip_install_via_setup_py() {
  pip install -e . --compile --force-reinstall --progress-bar pretty --log logfile5.txt
  # pip install -e . --compile --progress-bar pretty --log logfile5.txt
  pip check
}

function build_wheel() {
  #python -m build --wheel
  pip check
}

function main() {
  # setup_venv
  pip_compile
  pip_install
  pip_install_via_setup_py
  build_wheel
}

main
