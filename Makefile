.PHONY: ALL

clean:
	rm -rf cover .coverage */*.pyc */__pycache__

check: clean
	python manage.py test

check-model: clean
	python manage.py test eLocal_app/tests/model_tests.py

check-ui: clean
	python manage.py test eLocal_app/tests/ui_tests.py

