from git import Repo
import json


repo = Repo('../fastapi')
commits = repo.iter_commits()

json_file = []
for commit in commits:

    if commit.message.startswith(":"):
        message = commit.message.split()
        structured_message = {
            "emoji": message[0],
            "message": " ".join(message[1:])
        }
        json_file.append(structured_message)


with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(json_file, f, ensure_ascii=False, indent=4)