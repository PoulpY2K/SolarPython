main: setup
	python solar_system.py

setup: libs\dependencies.txt
	pip install -r libs\dependencies.txt

run: main