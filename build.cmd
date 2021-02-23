pip install -e . --compile --progress-bar pretty
pip install -q build
python -m build
pip install dist/artefact_content-0.0.18.whl
