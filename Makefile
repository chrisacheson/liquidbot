.PHONY: clean dev publish
DIST := dist

clean:
	rm -rf $(DIST)

build: clean
	python setup.py sdist

dev:
	python setup.py develop

publish: clean build
	twine upload $(DIST)/*

publish-test: clean build
	twine upload -r pypitest $(DIST)/*
