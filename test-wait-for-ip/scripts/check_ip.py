import time
import json
import socket

from cloudify import ctx
from cloudify.manager import get_rest_client
from cloudify_rest_client.executions import Execution


def wait_for_status(client, execution, timeout=10000):
    deadline = time.time() + timeout
    ctx.logger.info('checking execution {0} initail status {1}'.format(
        execution.id, execution.status))
    while execution.status not in Execution.END_STATES:
        time.sleep(2)
        execution = client.executions.get(execution.id)
        ctx.logger.info('after 2s execution.status {0}'.format(
            execution.status))
        if time.time() > deadline:
            raise Exception(
                    'Execution timed out: \n{0}'
                    .format(json.dumps(execution, indent=2)))
        if execution.status == Execution.FAILED:
            raise Exception(
                'Workflow execution failed: {0} [{1}]'.format(
                    execution.error,
                    execution.status))


def check_https(ip_address):
    try:
        # Attempt to create a connection to the IP address on port 443
        with socket.create_connection((ip_address, 443), timeout=5) as connection:
            return True
    except (socket.timeout, socket.error):
        return False


https_ready = False
while not https_ready:

    rest_client = get_rest_client()
    deployment_id = ctx.deployment.id
    workflow_id = 'execute_operation'
    parameters = {
        'operation': 'cloudify.interfaces.lifecycle.create',
        'node_instance_ids': [ctx.instance.id]
    }

    execution = rest_client.executions.start(deployment_id, workflow_id, parameters, force=True)
    wait_for_status(rest_client, execution)

    ctx.instance.refresh()
    ip = ctx.instance.runtime_properties['ip']
    ctx.logger.info('checking IP {0}'.format(ip))
    https_ready = check_https(ip)
    time.sleep(30)

