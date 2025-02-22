import json

def save_data(tasks, users):
    with open("data.json", "w") as f:
        json.dump({
            "tasks": tasks,
            "users": users
        }, f)

def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": [], "users": []}