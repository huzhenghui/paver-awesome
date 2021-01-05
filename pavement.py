import subprocess
from paver.easy import task
from paver.easy import cmdopts
from paver.easy import call_task
from paver.tasks import environment
from paver.shell import sh


@task
def default(options):
    call_task('choose_task')


@task
def paver_help(options):
    print("help")
    call_task("help", {})


def _task_list():
    def get_module_name(item):
        dotpos = item.name.rfind('.')
        return item.name[:dotpos]
    tasks = environment.get_tasks()  # type: set
    tasknames = []
    for taskitem in tasks:
        if "pavement" == get_module_name(taskitem):
            tasknames.append(taskitem.shortname)
    tasknames.sort()
    return tasknames


@task
def task_list(options):
    tasknames = _task_list()
    for taskname in tasknames:
        print(taskname)


@task
def ponysay_task_list(options):
    process = subprocess.Popen(
        ['ponysay'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    tasknames = _task_list()
    for taskname in tasknames:
        process.stdin.write(bytes(taskname + "\n", encoding='utf-8'))
    process.stdin.flush()
    process.stdin.close()
    lines = process.stdout.readlines()
    for line in lines:
        print(str(line, 'utf-8'), end='')


@task
def choose_task(options):
    # sh("/usr/local/opt/choose-gui/bin/choose")
    process = subprocess.Popen(
        ['/usr/local/opt/choose-gui/bin/choose'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    tasknames = _task_list()
    for taskname in tasknames:
        process.stdin.write(bytes(taskname + "\n", encoding='utf-8'))
    process.stdin.flush()
    process.stdin.close()
    lines = process.stdout.readlines()
    if 0 < len(lines):
        choose_task = str(lines[0], 'utf-8')
        if choose_task in tasknames:
            call_task(choose_task, {}, {})
