import os
import time

from cloudify import ctx
from cloudify.state import ctx_parameters
from cloudify import manager
from cloudify.utils import LocalCommandRunner

PROP_TO_UPDATE = ctx_parameters.get('property_to_update', '')
LIST_TO_SELECT_FROM = ctx_parameters.get('property_value_choice_input', '')

client = manager.get_rest_client()

file_to_block_parallel = '/tmp/prop_hack_{0}_{1}'.format(ctx.deployment.id, ctx.node.name)

ctx.logger.info('lock file {0}'.format(file_to_block_parallel))

while os.path.exists(file_to_block_parallel):
    time.sleep(2)
f = open(file_to_block_parallel, 'w')
f.close()

inputs = client.deployments.get(ctx.deployment.id).get('inputs')
exec_id = ctx.get_execution().get('id')
# override execution workflow_id temproary
x = LocalCommandRunner()
x.run('cfy_manager dbs shell "update executions set workflow_id=\'{0}\' where id =\'{1}\';"'.format('update', exec_id))

choices = inputs.get(LIST_TO_SELECT_FROM, [])
node_data = client.nodes.get(ctx.deployment.id, ctx.node.id)
node_data.get('properties', {})[PROP_TO_UPDATE] = choices[ctx.instance.index - 1]
node_data.pop('deployment_id', None)
client.nodes.update(ctx.deployment.id, ctx.node.id, **node_data)

x.run('cfy_manager dbs shell "update executions set workflow_id=\'{0}\' where id =\'{1}\';"'.format('install', exec_id))
os.remove(file_to_block_parallel)

# just in case setting the index 
ctx.instance.runtime_properties['index'] = ctx.instance.index - 1
ctx.instance.update()