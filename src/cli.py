import click
import json
from pathlib import Path

file_path = './tasks.JSON' 

def setup() -> None:
    # create file & write starter info on first install
    with open(file_path, "r+") as file:
        if Path(file_path).stat().st_size == 0:
            json.dump({"nextId":1}, file)
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
        # prevent creating duplicate tasks
        if description in tasks.values():
            click.echo("task already created")
            return

        # update nextId and add new task
        tasks["nextId"] += 1
        tasks[str(task_id)] = description

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
        
        if id not in tasks.keys():
            click.echo("task id invalid")
            return

        # update task description with new_description
        tasks[str(id)] = new_description

        # overwrite file
        file.seek(0)
        json.dump(tasks, file)
    
    click.echo(f"Task updated successfully")

@click.command()
@click.argument('id')
def delete(id: int) -> None:
    # read in tasks from file
    with open(file_path, "r+") as file:
        tasks = json.load(file)
        
        if id not in tasks.keys():
            click.echo("task id does not exist")
            return

        # update task description with new_description
        tasks.pop(str(id))

        # overwrite file
        file.seek(0)
        json.dump(tasks, file)
    
    click.echo(f"Task deleted successfully")

@click.command()
def clear() -> None:
    with open(file_path, "w") as file:
        json.dump({"nextId":1}, file)
        click.echo('Tasks cleared!')
    

@click.command()
@click.argument('id')
def mark_in_progress(id) -> None:
    # TODO
    pass

@click.command()
@click.argument('id')
def mark_done(id) -> None:
    # TODO
    pass

@click.option('--done', help='completed tasks')
@click.option('--todo', help='tasks that need to be completed')
@click.option('--in-progress', help='tasks actively being worked on')
@click.command()
def list() -> None:
    # TODO
    pass



# add all commands to main group
cli.add_command(add)
cli.add_command(update)
cli.add_command(delete)
cli.add_command(clear)
cli.add_command(mark_in_progress)
cli.add_command(mark_done)
cli.add_command(list)

# TODO: replace with toml entrypoint 
if __name__ == '__main__':
    cli()