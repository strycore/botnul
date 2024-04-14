deps:
	pip install -r requirements.txt


run:
	python3 botnul.py


deploy:
	rsync -avz --exclude __pycache__ .  strycore.com:botnul/