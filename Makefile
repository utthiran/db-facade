build:
	python setup.py sdist bdist_wheel

publish-testpypi:
	twine upload --repository testpypi dist/*

publish-pypi:
	twine upload --repository pypi dist/*

remove-old-build:
	rm -rf build dist db_facade.egg-info