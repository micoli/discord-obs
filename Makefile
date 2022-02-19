init:
	pip3 install -e ".[testing]"

clean:
	find . -name "__pycache__" | xargs rm -r
