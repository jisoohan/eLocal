runtest  = python manage.py test
root  = eLocal_app/tests
utils = $(root)/utils_tests.py
views = $(root)/view_tests.py
ui    = $(root)/ui_tests.py

.PHONY: ALL

clean:
	rm -rf cover .coverage */*.pyc */__pycache__

check: clean
	$(runtest)

check-unit check-units: clean
	$(runtest) $(utils) $(views)

check-ui: clean
	$(runtest) $(ui)

check-util check-utils: clean
	$(runtest) $(utils)

check-view check-views: clean
	$(runtest) $(views)

