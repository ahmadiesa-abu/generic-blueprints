import time
import json

from cloudify.workflows import ctx
from cloudify.manager import get_rest_client
from cloudify_rest_client.executions import Execution


def wait_for_status(client, execution, timeout=10000):
    deadline = time.time() + timeout
    ctx.logger.info('checking execution {0} initail status {1}'.format(execution.id, execution.status))
    while execution.status not in Execution.END_STATES:
        time.sleep(20)
        execution = client.executions.get(execution.id)
        ctx.logger.info('after 20s execution.status {0}'.format(execution.status))
        if time.time() > deadline:
            raise Exception(
                    'Execution timed out: \n{0}'
                    .format(json.dumps(execution, indent=2)))
        if execution.status == Execution.FAILED:
            raise Exception(
                'Workflow execution failed: {0} [{1}]'.format(
                    execution.error,
                    execution.status))


rest_client = get_rest_client()
executions = []

for instance in ctx.node_instances:
    deployment_id = instance.runtime_properties['deployment']['id']
    execution = rest_client.executions.start(deployment_id, 'some_wf')
    executions.append(execution)

for execution in executions:
    wait_for_status(rest_client, execution)
    ctx.logger.info("workflow {} installed".format(execution.deployment_id))
