main:
	python solar_system.py

data:
	python api.py

setup: libs\dependencies.txt
	pip install -r libs\dependencies.txt

run: setup data main clean