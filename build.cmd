rem deactivate
rem rm -rf venv
rem py -3 -m venv venv
rem venv\Scripts\activate

pip-compile -r requirements\build.in
pip-compile -r requirements\docs.in
pip-compile -r requirements\tests.in
pip-compile -r requirements\dev.in

pip install -r requirements\build.in  --log logfile1.txt
pip install -r requirements\docs.in  --log logfile2.txt
pip install -r requirements\tests.in --log logfile3.txt
pip install -r requirements\dev.in --log logfile4.txt

rem pip install -r requirements\dev.in --force-reinstall --use-pep517 --no-cache-dir --compile --progress-bar pretty --log logfile1.txt
rem pip install -r requirements\dev.in --use-pep517 --progress-bar pretty --log logfile1.txt
rem pip install -e . --force-reinstall --use-pep517 --no-cache-dir --compile --progress-bar pretty --log logfile2.txt
rem pip install -q build --implementation py  --python-version 3.8 --user --force-reinstall --use-pep517 --compile --progress-bar pretty

pip install -e . --compile --force-reinstall --progress-bar pretty --log logfile5.txt

python -m build --wheel
