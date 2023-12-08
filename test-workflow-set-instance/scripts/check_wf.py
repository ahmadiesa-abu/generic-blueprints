from cloudify.workflows import ctx

ctx.logger.info('deployment_id {0}'.format(ctx.deployment.id))


for instance in ctx.node_instances:
    runtime_properties = instance._node_instance.runtime_properties
    runtime_properties['terraform_version'] = {}
    ctx.update_node_instance(node_instance_id=instance.id,
                             runtime_properties=runtime_properties,
                             version=instance._node_instance.version)