.PHONY: ALL

clean:
	rm -rf cover .coverage */*.pyc */__pycache__

check: clean
	python manage.py test

check-model: clean
	python manage.py test eLocal_app/tests/model_tests.py

check-ui: clean
	python manage.py test eLocal_app/tests/ui_tests.py

check-util: clean
	python manage.py test eLocal_app/tests/utils_tests.py

check-view: clean
	python manage.py test eLocal_app/tests/view_tests.py

