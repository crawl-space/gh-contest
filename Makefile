run:
	python main.py download/{data,repos,lang,test}.txt results.txt

test-data:
	mkdir -p dummy
	python make-test-data.py filtered.txt download/{repos,lang}.txt dummy

run-dummy: test-data
	python main.py dummy/data.txt download/{repos,lang}.txt dummy/test.txt \
		results-dummy.txt

eval-dummy: run-dummy
	python evaluate-results.py dummy/target.txt results-dummy.txt
