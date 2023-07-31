from fabric2 import task

from cloudify import ctx
from cloudify.state import current_ctx

import inspect

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec


@task
def check_drift(connection):
    command = 'echo "in check_drift"'
    result = connection.run(command)
    return False



@task
def update(connection):
    command = 'echo "in update"'
    connection.run(command)
