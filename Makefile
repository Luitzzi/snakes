venv:
	python -m venv venv && source venv/bin/activate

install:
	pip install -r requirements.txt

lint:
	ruff check .

run:
	python main.py
