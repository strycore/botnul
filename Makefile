deps:
	pip install -r requirements.pip

run:
	python3 botnul.py

deploy:
	rsync -avz --exclude __pycache__ .  strycore.com:botnul/

sync_backups:
	rsync -avz "strycore.com:botnul/*.json" .