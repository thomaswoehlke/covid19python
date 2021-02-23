rem .\venv\Scripts\activate
pip install -r requirements\dev.in --user --force-reinstall --use-pep517 --no-cache-dir --compile --progress-bar pretty --log logfile1.txt
pip install -e . --user --force-reinstall --use-pep517 --no-cache-dir --compile --progress-bar pretty --log logfile2.txt
rem pip install -q build --implementation py  --python-version 3.8 --user --force-reinstall --use-pep517 --compile --progress-bar pretty
rem python -m build
rem pip install -e . --compile --progress-bar pretty
pip install dist/covid19python-0.0.19.whl --progress-bar pretty --log logfile3.txt
