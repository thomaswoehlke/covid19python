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

rem pip install -e . --compile --force-reinstall --progress-bar pretty --log logfile5.txt
pip install -e . --compile --progress-bar pretty --log logfile5.txt

rem python -m build --wheel
