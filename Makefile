run:
	PYTHONPATH=. python bin/main.py download/{data,repos,lang,test}.txt \
			   results.txt

test-data:
	mkdir -p dummy
	PYTHONPATH=. python bin/make-test-data.py filtered.txt \
			   download/{repos,lang}.txt dummy

run-dummy: test-data
	PYTHONPATH=. python bin/main.py dummy/data.txt download/{repos,lang}.txt \
			   dummy/test.txt results-dummy.txt

eval-dummy: run-dummy
	PYTHONPATH=. python bin/evaluate-results.py dummy/target.txt \
			   results-dummy.txt

stats:
	PYTHONPATH=. python bin/print-stats.py download/{data,repos,lang}.txt
