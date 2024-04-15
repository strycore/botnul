import json

user_id = 111111111111111111
backup_filename = "backup-home.json"
dest_filename = "quotes-nickname.txt"

with open(backup_filename) as backup_file:
    messages = json.load(backup_file)

quotes = []

with open(dest_filename, "w", encoding="utf-8") as dest_file:
    for message in messages:
        if message["author"]["id"] != user_id:
            continue
        if not message["content"]:
            continue
        dest_file.write(message["content"] + "\n")
