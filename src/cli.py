import click
import json
from pathlib import Path

file_path = './tasks.JSON' 

def setup() -> None:
    # create file & write starter info on first install
    with open(file_path, "r+") as file:
        if Path(file_path).stat().st_size < 56:
            json.dump({"nextId":1, "done": {}, "todo": {}, "in-progress": {}}, file)
            click.echo('setup template file')
            click.echo('Let\'s get something done!')
        
@click.group()
def cli() -> None:
    setup()

@click.command()
@click.argument('description')
def add(description) -> None:
    # read in tasks from file
    with open(file_path, "r+") as file:
        tasks = json.load(file)
        task_id = tasks["nextId"]
        todo = tasks["todo"]
        # prevent creating duplicate tasks
        if description in tasks.values():
            click.echo("task already created")
            return

        # update nextId and add new task
        tasks["nextId"] += 1
        todo[str(task_id)] = description

        # overwrite file with new tasks
        file.seek(0)
        json.dump(tasks, file)
    
    click.echo(f"Task added successfully (ID:{task_id})")

@click.command()
@click.argument('id')
@click.argument('new_description')
def update(id: int, new_description: str) -> None:
    # read in tasks from file
    with open(file_path, "r+") as file:
        tasks = json.load(file)
        todo = tasks["todo"]
        in_progress = tasks['in-progress']
        done = tasks['done']
        
        if str(id) not in tasks.keys():
            click.echo("task id invalid")
            return

        # update task description with new_description
        todo[str(id)] = new_description
        if str(id) in in_progress.keys():
            in_progress[str(id)] = new_description
        if str(id) in done.keys():
            done[str(id)] = new_description

        # overwrite file
        file.seek(0)
        json.dump(tasks, file)
        file.truncate()
    
    click.echo(f"Task updated successfully")

@click.command()
@click.argument('id')
def delete(id: int) -> None:
    # read in tasks from file
    with open(file_path, "r+") as file:
        tasks = json.load(file)
        todo = tasks["todo"]
        in_progress = tasks['in-progress']
        done = tasks['done']
        
        if str(id) not in todo.keys():
            click.echo("task id does not exist")
            return

        # update task description with new_description
        todo.pop(str(id))
        if str(id) in in_progress.keys():
            in_progress.pop(str(id))
        if str(id) in done.keys():
            done.pop(str(id))

        # overwrite file
        file.seek(0)
        json.dump(tasks, file)
        file.truncate()
    
    click.echo(f"Task deleted successfully")

@click.command()
def clear() -> None:
    with open(file_path, "w") as file:
        json.dump({"nextId":1, "done": {}, "todo": {}, "in-progress": {}}, file)
        click.echo('Tasks cleared!')
    

@click.command()
@click.argument('id')
def mark_in_progress(id: int) -> None:
    with open(file_path, "r+") as file:
        tasks = json.load(file)
        todo = tasks["todo"]
        in_progress = tasks['in-progress']
        done = tasks['done']
        
        if str(id) not in todo.keys():
            click.echo("task id invalid")
            return
        
        #add to in-progress, remove from done if necessary
        if str(id) in done.keys():
            done.pop(str(id))
        in_progress[str(id)] = todo[str(id)]

        # overwrite file
        file.seek(0)
        json.dump(tasks, file)
        file.truncate()
    
    click.echo(f"Marked task {id} in progress")

@click.command()
@click.argument('id')
def mark_done(id) -> None:
    with open(file_path, "r+") as file:
        tasks = json.load(file)
        todo = tasks["todo"]
        in_progress = tasks['in-progress']
        done = tasks['done']
        
        if str(id) not in todo.keys():
            click.echo("task id invalid")
            return
        
        #add to in-progress, remove from done if necessary
        if str(id) in in_progress.keys():
            in_progress.pop(str(id))
        done[str(id)] = todo[str(id)]

        # overwrite file
        file.seek(0)
        json.dump(tasks, file)
        file.truncate()
    
    click.echo(f"Task updated successfully")


@click.command()
@click.option('--done', is_flag=True, help='completed tasks')
@click.option('--todo', is_flag=True, help='tasks that need to be completed')
@click.option('--in-progress', 'in_progress', is_flag=True, help='tasks actively being worked on')
def list_tasks(done: bool, todo: bool, in_progress: bool) -> None:
    selected = sum([done, todo, in_progress])

    if selected != 1:
        raise click.UsageError("Pass exactly one of: --todo, --done, --in-progress")

    with open(file_path, "r") as file:
        tasks = json.load(file)

    lst = {}
    if done:
        lst = tasks["done"]
    elif todo:
        lst = tasks["todo"]
    else:
        lst = tasks["in-progress"]

    for val in lst.values():
        print(val)
        
# add all commands to main group
cli.add_command(add)
cli.add_command(update)
cli.add_command(delete)
cli.add_command(clear)
cli.add_command(mark_in_progress)
cli.add_command(mark_done)
cli.add_command(list_tasks)

# TODO: replace with toml entrypoint 
if __name__ == '__main__':
    cli()