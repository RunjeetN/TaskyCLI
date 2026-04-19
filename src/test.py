import json
from pathlib import Path
file_path = './tasks.JSON'


p = Path(".")
tasks = {}

# open or create file
with open(file_path, "w") as file:
    # if file is empty:
    if Path(file_path).stat().st_size == 0:
        # write {"nextId": 1} as json with json.dumps()
        json.dump({"nextId":1}, file)
# read file content to dictionary with json.loads()
with open(file_path, "r") as file:
    tasks = json.load(file)
    
print(tasks)


print([x for x in p.iterdir()])