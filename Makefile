SHELL := /bin/bash

instantionate-local: instantionate-.env instantionate-python

instantionate-.env:
	cp .env auth
	cp .env mcli
	cp .env playlist
	cp .env subcription

instantionate-python:
	pip install virtualenv

	virtualenv auth/venv
	auth/venv/bin/pip install -r auth/requirements.txt

	virtualenv mcli/venv
	auth/venv/bin/pip install -r auth/requirements.txt

	virtualenv playlist/venv
	playlist/venv/bin/pip install -r auth/requirements.txt

	virtualenv subcription/venv
	subcription/venv/bin/pip install -r auth/requirements.txt

cleanup:
	rm -r auth/venv
	rm -r mcli/venv
	rm -r playlist/venv
	rm -r subcription/venv

	rm auth/.env
	rm mcli/.env
	rm playlist/.env
	rm subcription/.env
