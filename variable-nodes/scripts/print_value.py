from cloudify import ctx

node_instance_index = ctx.instance.runtime_properties['index']
if isinstance(ctx.node.properties['some_number'], list):
    size_wanted = ctx.node.properties['some_number'][node_instance_index]
else:
    ctx.logger.info('here with the new value')
    size_wanted = ctx.node.properties['some_number']
ctx.logger.info('size_wanted : {0}'.format(size_wanted))
