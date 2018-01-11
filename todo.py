import click
import json


def readDataFromJson():
    try:
        with open('/home/cameron/todolist.json', 'r') as f:
            data = json.load(f)
        f.close()
        return data
    except:
        click.echo("Could not open the JSON file for reading!")
        return None

def writeDatatoJson(data):
    try:
        f = open('/home/cameron/todolist.json', 'w+')
    except:
        click.echo("Could not open the JSON file for writing")
        exit(1)

    json.dump(data, f, separators=(',', ':'), indent=4)
    f.close()


def printList():
    data = readDataFromJson()
    if data is None:
        exit(1)

    lists = data[1]
    click.echo()
    for tasklist in lists:
         click.secho(tasklist.upper(), fg="green", bold=True)
         for task in lists[tasklist]:
             info = lists[tasklist][task]
             if info['completed']:
                 comp = 'X'
             else:
                 comp = ' '
             click.echo("%s\t[%s]\t%10s\t%-20s\t%s" % (info['id'], comp, info['due'], task, info['description']))
         click.echo()



@click.group()
def cli():
    '''Todo-list command line application'''
    pass


@cli.command()
@click.option('-l', '--listname', help='The list to add the task to', prompt='List')
@click.option('-d', '--due', help="The date which this task is to be completed", prompt="Due")
@click.option('-s', '--description', help="Description of the task", prompt='Description')
@click.argument('taskname', nargs=-1)
def add(listname, taskname, due, description):
    '''Add a task to a certain list'''

    try:
        with open('/home/cameron/todolist.json', 'r') as f:
            data = json.load(f)
        f.close()
    except (ValueError, IOError):
        data = [0, {}]
    except:
        click.echo("Could not open the JSON file for reading")
        click.echo(e)
        exit(1)

    numTasks = data[0]
    listInfo = data[1]
    listname = listname.lower().strip()
    taskname = " ".join(taskname)

    #add the task to the list, create a new list if it doesn't already exist
    if listname not in listInfo:
        listInfo[listname] = {}
    elif taskname in listInfo[listname]:
            click.echo("This task name already exists")
            exit(1)


    listInfo[listname][taskname] = {"description": description, "due": due, "id": numTasks+1, "completed": False}

    data[0] = data[0] + 1

    #save the new task in the JSON file
    writeDatatoJson(data)

    click.echo()
    click.echo('Added task %s (%s) to list %s, due %s' % (taskname, description, listname, due))
    printList()

@cli.command()
@click.argument("id")
def rm(id):
    '''Remove a task by its ID'''
    data = readDataFromJson()

    found = False
    for listName in data[1]:
        for task in data[1][listName]:
            info = data[1][listName][task]
            if info['id'] == int(id):
                data[1][listName].pop(task, None)
                if len(data[1][listName]) == 0:
                    data[1].pop(listName, None)
                data[0] -= 1
                found = True
                break
        if found:
            break

    if not found:
        click.echo("Could not find task %s" % id)
    else:
        click.echo("Removed task %s" % id)
        #decrement the higher ids
        for lst in data[1]:
            for task in data[1][lst]:
                if data[1][lst][task]['id'] > int(id):
                    data[1][lst][task]['id'] -= 1

        writeDatatoJson(data)
        printList()

@cli.command()
@click.argument('id')
def com(id):
    '''Complete a task by its ID'''
    data = readDataFromJson()

    found = False
    for listName in data[1].keys():
        for task in data[1][listName].keys():
            info = data[1][listName][task]
            if info['id'] == int(id):
                data[1][listName][task]['completed'] = True
                click.echo("Marked task %s as complete" % id)
                found = True
                break;
        if found:
            break;

    if not found:
        click.echo("Could not find task %s" % id)
    else:
        writeDatatoJson(data)
        printList()

@cli.command()
@click.argument('id')
def uncom(id):
    '''Mark a task as uncomplete by its ID'''
    data = readDataFromJson()

    found = False
    for listName in data[1].keys():
        for task in data[1][listName].keys():
            info = data[1][listName][task]
            if info['id'] == int(id):
                data[1][listName][task]['completed'] = False
                click.echo("Marked task %s as uncomplete" % id)
                found = True
                break;
        if found:
            break;

    if not found:
        click.echo("Could not find task %s" % id)
    else:
        writeDatatoJson(data)
        printList()

@cli.command()
#TODO: make an option for sorting the list contents/filter results
def list():
    '''Output current tasks and lists'''
    printList()


@cli.command()
@click.confirmation_option(prompt="Are you sure you want to delete all tasks?")
def clear():
    '''Clear all tasks'''
    try:
        f = open('/home/cameron/todolist.json', 'r')
        data = json.load(f)
        f.close()
    except ValueError as e:
        click.echo("There are no tasks to clear")
        exit(1)
    except:
        click.echo("Could not read the JSON file. Check that one exisits.")
        exit(1)

    if data[0] == 0:
        click.echo("There are no tasks to clear")
    else:
        try:
            f = open('/home/cameron/todolist.json', 'w')
            json.dump([0, {}], f, separators=(',', ':'), indent=4)
            f.close()
            click.echo("Cleared all tasks")
        except IOError:
            click.echo("Could not write to the JSON file")
            exit(1)
