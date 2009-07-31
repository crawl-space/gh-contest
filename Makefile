run:
	python main.py download/{data,repos,lang,test}.txt results.txt

test-data:
	python make-test-data.py filtered.txt download/{repos,lang}.txt dummy
