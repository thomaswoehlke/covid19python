cat requirements/build.txt | grep -v '#' | sed 's/^/\t"/g' | sed 's/$/",/g' > requirements/req_build.py
cat requirements/docs.txt | grep -v '#' | sed 's/^/\t"/g' | sed 's/$/",/g' > requirements/req_docs.py
cat requirements/tests.txt | grep -v '#' | sed 's/^/\t"/g' | sed 's/$/",/g' > requirements/req_tests.py
cat requirements/dev.txt | grep -v '#' | sed 's/^/\t"/g' | sed 's/$/",/g' > requirements/req_dev.py
