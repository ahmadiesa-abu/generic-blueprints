import time
import json

from cloudify.workflows import ctx
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


def get_ordered_child_deployment(deployment_id):
    ordered_dep = []
    child_deployments = {}

    graph = ctx.graph_mode()
    subgraphs = {}

    original_dep_id = ctx._context['deployment_id']
    try:
        ctx._context['deployment_id'] = deployment_id
        ctx.internal.handler._rest_client = get_rest_client('test')
        ctx.refresh_node_instances()
        for instance in ctx.node_instances:
            deploy_id = instance.runtime_properties['deployment']['id']
            child_deployments[instance.id] = deploy_id
            subgraphs[instance.id] = graph.subgraph(instance.id)
        for instance in ctx.node_instances:
            for rel in instance.relationships:
                graph.add_dependency(subgraphs[instance.id],
                                     subgraphs[rel.target_id])
    finally:
        ctx._context['deployment_id'] = original_dep_id
        ctx.internal.handler._rest_client = get_rest_client()
        ctx.refresh_node_instances()

    ordered_instances = [instance.name for instance in graph.linearize()]
    for instance in ordered_instances:
        ordered_dep.append(child_deployments[instance])
    return ordered_dep


rest_client = get_rest_client('test')
executions = []

for instance in ctx.node_instances:
    if instance.node.type != 'cloudify.nodes.ServiceComponent':
        continue
    deployment_id = instance.runtime_properties['deployment']['id']
    ordered_dep = get_ordered_child_deployment(deployment_id)
    for dep in ordered_dep:
        ctx.logger.info('running execution on dep {0}'.format(dep))
        execution = rest_client.executions.start(dep, 'some_wf')
        wait_for_status(rest_client, execution)
