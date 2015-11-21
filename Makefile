runtest  = python manage.py test
root  = eLocal_app/tests
model = $(root)/model_tests.py
utils = $(root)/utils_tests.py
views = $(root)/view_tests.py
ui    = $(root)/ui_tests.py

.PHONY: ALL

clean:
	rm -rf cover .coverage */*.pyc */__pycache__

check: clean
	$(runtest)

check-unit check-units: clean
	$(runtest) $(model) $(utils) $(views)

check-model check-models: clean
	$(runtest) $(model)

check-ui: clean
	$(runtest) $(ui)

check-util check-utils: clean
	$(runtest) $(utils)

check-view check-views: clean
	$(runtest) $(views)

