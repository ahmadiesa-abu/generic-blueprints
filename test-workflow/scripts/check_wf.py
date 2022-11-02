from cloudify.workflows import ctx

ctx.logger.info('deployment_id {0}'.format(ctx.deployment.id))