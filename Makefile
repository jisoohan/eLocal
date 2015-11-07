.PHONY: ALL

clean:
	rm -rf cover .coverage */*.pyc */__pycache__

check: clean
	python manage.py test

