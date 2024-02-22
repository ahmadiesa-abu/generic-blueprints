from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.manager import get_rest_client

rest_client = get_rest_client()
deployment_id = ctx.deployment.id
node_instances = rest_client.node_instances.list(deployment_id=deployment_id, _get_all_results=True)

depend_on_node_id = None

ctx.logger.info('ctx.instance.relationships {0}'.format(ctx.instance.relationships))

for relation in ctx.instance.relationships:
    if relation.type == 'cloudify.relationships.depends_on':
        ctx.logger.info('relation_target {0}'.format(relation.target))
        depend_on_node_id = relation.target.node.id

if depend_on_node_id == None:
    ctx.instance.runtime_properties['ip'] = inputs.get('some_ip')
else:
    for node in node_instances:
        if node.get('node_id') == depend_on_node_id:
            ctx.instance.runtime_properties['ip'] = node.runtime_properties['ip']
