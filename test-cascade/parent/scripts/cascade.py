from time import sleep
from cloudify.workflows import ctx
from cloudify.manager import get_rest_client


def wait_for_status(client, execution, timeout=10000):
    counter = timeout
    wrong_state = ['failed',  'cancelled']
    in_progress_state = ['pending', 'started']
    while execution.status not in in_progress_state and timeout > 0:
        sleep(20)
        counter = counter - 20
        execution = client.executions.get(execution.id)

    if counter <= 0:
        raise Exception(
            "Execution {} is in {} state "
            "for longer than the timeout {}s".format(execution.id,
                                                     execution.status,
                                                     timeout))
    elif counter > 0 and execution.status in wrong_state:
        raise Exception(
            "Execution {} is in {} state ".format(
                execution.id,
                execution.status,
                timeout))

rest_client = get_rest_client()
executions = []

for instance in ctx.node_instances:
    deployment_id = instance.runtime_properties['deployment']['id']
    execution = rest_client.executions.start(deployment_id, 'some_wf')
    executions.append(execution)

for execution in executions:
    wait_for_status(rest_client, execution)
    ctx.logger.info("workflow {} installed".format(execution.deployment_id))
